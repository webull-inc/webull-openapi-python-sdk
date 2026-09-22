# Copyright 2022 Webull
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding=utf-8
import json
import logging
import os
import ssl
import threading
import time

import httpx

from webull.core.auth.algorithm import sha_hmac256_new
from webull.core.common import api_type
from webull.core.endpoint.default_endpoint_resolver import \
    DefaultEndpointResolver
from webull.core.endpoint.resolver_endpoint_request import \
    ResolveEndpointRequest
from webull.core.exception import error_code
from webull.core.exception.exceptions import ClientException, ServerException
from webull.core.retry.retry_condition import RetryCondition
from webull.core.sse.default_retry_policy import DefaultSseSubscribeRetryPolicy, SseSubscribeRetryPolicyContext
from webull.core.sse.signature_composer import calc_signature
from webull.core.sse.sse_parser import iter_sse_frames
from webull.core.sse.subscribe_response import SseSubscribeResponse, EVENT_SUBSCRIBE_SUCCESS, EVENT_PING, \
    EVENT_BUSINESS, EVENT_AUTH_ERROR, EVENT_NUM_OF_CONN_EXCEED, EVENT_SUBSCRIBE_EXPIRED
from webull.core.utils import common as core_common
import webull.core.headers as hd

# contentTypes
JSON = "application/json"
TEXT = "text/plain"

DEFAULT_REGION_ID = "us"
DEFAULT_SUBSCRIBE_PATH = "/subscribe/sse"
# 1 2 4 allowed now, 7 subscribes order, position and option at once
DEFAULT_SUBSCRIBE_TYPE = 7
DEFAULT_CONNECT_TIMEOUT = 10
# Server writes a ": heartbeat" comment line every 20s by default, give up
# after two missed heartbeats and let the retry policy rebuild the subscription.
DEFAULT_READ_TIMEOUT = 45
MAX_ERROR_BODY_LENGTH = 512
ACCEPT_EVENT_STREAM = "text/event-stream"


def _mask(value, prefix_length=6):
    """Keep only a short prefix of a credential like value for logging."""
    if not value:
        return value
    return value[:prefix_length] + "***"


class TradeEventsSseClient:
    """Trade events subscription over the SSE channel.

    Drop in alternative to ``TradeEventsClient``: callbacks, logging hooks and
    the retry mechanism keep the same shape, only the transport differs
    (HTTP text/event-stream instead of gRPC server streaming).

    Note that subscriptions are mutually exclusive per app key across both
    channels. While another subscription of the same app key is active, the
    new SSE subscribe request is rejected (the active one is not affected),
    either with HTTP 429 before the stream is established, or with a
    ``numOfConnExceed`` frame right after it. Both cases are retried with
    jittered exponential backoff.

    ``authError`` and ``subscribeExpired`` frames require client side action
    (fix the credentials, renew the subscription), reconnecting with the same
    credentials would fail again. They are passed to ``on_fatal_error``; the
    subscription stops and raises ``ServerException`` unless the callback
    returns True, in which case it keeps reconnecting with backoff (e.g. while
    waiting for a renewal of the same app key).

    Only stream closes and transport failures are reconnected. Exceptions
    raised by ``on_connect`` / ``on_events_message`` or by decoding a JSON
    payload stop the subscription and are re-raised by ``do_subscribe``, the
    same as ``TradeEventsClient``.
    """

    def __init__(self, app_key, app_secret, region_id=DEFAULT_REGION_ID, host=None, port=443,
                 tls_enable=True, retry_policy=None, subscribe_type=DEFAULT_SUBSCRIBE_TYPE,
                 subscribe_path=DEFAULT_SUBSCRIBE_PATH, signer_spec=sha_hmac256_new,
                 connect_timeout=DEFAULT_CONNECT_TIMEOUT, read_timeout=DEFAULT_READ_TIMEOUT,
                 verify=None):
        self._app_key = app_key
        self._app_secret = app_secret
        self._region_id = region_id
        self._tls_enable = tls_enable
        self._endpoint_resolver = DefaultEndpointResolver(self)
        if not host:
            endpoint_request = ResolveEndpointRequest(
                self._region_id, api_type=api_type.EVENTS)
            endpoint = self._endpoint_resolver.resolve(endpoint_request)
            self._host = endpoint
        else:
            self._host = host
        self._port = port
        if retry_policy:
            self._retry_policy = retry_policy
        else:
            self._retry_policy = DefaultSseSubscribeRetryPolicy()
        self._subscribe_type = subscribe_type
        self._subscribe_path = subscribe_path
        self._signer_spec = signer_spec
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._verify = verify

        self._logger = None
        self._in_callback_mutex = threading.Lock()
        self._callback_mutex = threading.RLock()
        # callbacks
        self._on_connect = None
        self._on_events_message = None
        self._on_fatal_error = None
        self._on_log = None
        # Last control frame of the current stream that ends the
        # subscription (numOfConnExceed, authError, subscribeExpired).
        self._fatal_response = None
        # Whether the current stream received a subscribeSuccess frame.
        self._stream_subscribed = False

    def _get_url(self):
        scheme = "https" if self._tls_enable else "http"
        return "%s://%s:%s%s" % (scheme, self._host, self._port, self._subscribe_path)

    def _get_verify_value(self):
        verify = self._verify
        if verify is None:
            verify = os.environ.get('WEBULL_API_CA_BUNDLE', True)
        # httpx deprecates a CA bundle path as the verify value, wrap it in an
        # SSL context instead.
        if isinstance(verify, str):
            return ssl.create_default_context(cafile=verify)
        return verify

    def _build_request(self, accounts):
        """Build the request body and headers of one subscribe attempt.

        The signature covers the exact body bytes being sent, so the body is
        serialized once and reused for both signing and sending.
        """
        body = {
            "subscribeType": self._subscribe_type,
            "timestamp": int(time.time() * 1000),  # millis
            "accounts": list(accounts),
        }
        body_string = core_common.json_dumps_compact(body)
        body_bytes = body_string.encode("utf-8")
        signature, headers = calc_signature(
            self._app_key, self._app_secret, body_bytes, self._signer_spec)
        request_id = core_common.get_uuid()
        headers[hd.REQUEST_ID] = request_id
        headers[hd.NATIVE_CONTENT_TYPE] = JSON
        headers["Accept"] = ACCEPT_EVENT_STREAM
        self._easy_log(logging.DEBUG,
                       "sse subscribe request, url:%s, request_id:%s, body:%s, signature:%s",
                       self._get_url(), request_id, body_string, _mask(signature))
        return body_bytes, headers

    def _read_error_body(self, response):
        try:
            # Streamed responses must be read before the body is accessible.
            response.read()
            content = response.text
        except Exception as err:
            return "failed to read error body:%s" % err
        if content and len(content) > MAX_ERROR_BODY_LENGTH:
            return content[:MAX_ERROR_BODY_LENGTH]
        return content

    def _to_server_exception(self, response, error_body):
        error_code = str(response.status_code)
        error_msg = error_body
        if error_body:
            try:
                decoded = json.loads(error_body)
                if isinstance(decoded, dict) and "error" in decoded:
                    error_msg = decoded["error"]
            except ValueError:
                pass
        return ServerException(error_code, error_msg, http_status=response.status_code,
                               request_id=response.headers.get(hd.REQUEST_ID))

    def _to_fatal_exception(self, response):
        """Turn a fatal control frame into a ``ServerException``.

        The error code is the SSE frame name (e.g. ``subscribeExpired``) and
        the message is the frame payload, a human readable reason.
        """
        return ServerException(response.event, response.payload,
                               http_status=httpx.codes.OK, request_id=response.requestId)

    def _stream_processing(self, session, accounts):
        """Implementation of subscription logic.

        Args:
            session: an ``httpx.Client`` with HTTP/2 enabled. HTTP/2 is
                negotiated through TLS ALPN, the client falls back to HTTP/1.1
                when the server does not offer HTTP/2 or TLS is disabled.
            accounts: account IDs to subscribe.
        """
        url = self._get_url()
        timeout = httpx.Timeout(self._read_timeout, connect=self._connect_timeout)
        retry_policy_context = SseSubscribeRetryPolicyContext(None, 0, None)
        retries = 0
        final_exception = None
        while True:
            self._fatal_response = None
            self._stream_subscribed = False
            body_bytes, headers = self._build_request(accounts)
            try:
                request = session.build_request("POST", url, headers=headers,
                                                content=body_bytes, timeout=timeout)
                response = session.send(request, stream=True)
                try:
                    if response.status_code != httpx.codes.OK:
                        error_body = self._read_error_body(response)
                        final_exception = self._to_server_exception(response, error_body)
                        retry_policy_context = SseSubscribeRetryPolicyContext(
                            final_exception, retries, response.status_code)
                        self._easy_log(logging.ERROR,
                                       "sse subscribe failed, http status:%s, error:%s",
                                       response.status_code, error_body)
                    else:
                        self._easy_log(logging.INFO, "sse stream established, url:%s, http_version:%s",
                                       url, response.http_version)
                        for event, data in iter_sse_frames(response.iter_lines()):
                            self._easy_handler(event, data)
                            if self._fatal_response is not None:
                                # The server closes the stream right after a
                                # fatal frame, stop reading it.
                                break
                        # The server closed the stream, this channel has no
                        # resume support so a new subscription is required.
                        final_exception = None
                        retry_policy_context = SseSubscribeRetryPolicyContext(
                            None, retries, None)
                        self._easy_log(logging.WARNING, "sse stream closed by server")
                finally:
                    response.close()
            except httpx.HTTPError as request_error:
                final_exception = request_error
                retry_policy_context = SseSubscribeRetryPolicyContext(
                    request_error, retries, None)
                self._easy_log(logging.ERROR, "sse request error:%s", request_error)
            except Exception as exception:
                final_exception = exception
                retry_policy_context = SseSubscribeRetryPolicyContext(
                    exception, retries, None)
                self._easy_log(logging.ERROR, "sse exception:%s", exception)
            # The subscription succeeded on this attempt, count consecutive
            # failures from scratch whatever ended the stream (server close,
            # read timeout, connection reset). A 200 stream without
            # subscribeSuccess (e.g. numOfConnExceed) keeps the backoff going.
            if self._stream_subscribed:
                retries = 0
                retry_policy_context.retries_attempted = 0
            retryable = self._retry_policy.should_retry(retry_policy_context)
            fatal_response = self._fatal_response
            if fatal_response is not None:
                final_exception = self._to_fatal_exception(fatal_response)
                retry_policy_context.exception = final_exception
                if fatal_response.event != EVENT_NUM_OF_CONN_EXCEED \
                        and not self._handle_fatal_error(fatal_response):
                    self._easy_log(
                        logging.ERROR, "processing stopped due to fatal frame, response:%s",
                        fatal_response)
                    break
                # Mutex rejections share the backoff of HTTP 429, and so do
                # the reconnects requested by on_fatal_error.
                retryable |= RetryCondition.SHOULD_RETRY_WITH_THROTTLING_BACKOFF
            if retryable & RetryCondition.NO_RETRY:
                self._easy_log(
                    logging.ERROR, "processing stopped, not retryable, retry_context:%s",
                    retry_policy_context)
                break
            retry_policy_context.retryable = retryable
            time_to_sleep = self._retry_policy.compute_delay_before_next_retry(
                retry_policy_context)
            self._easy_log(logging.INFO, "next retry will be started in %s ms, retry_context:%s",
                           time_to_sleep, retry_policy_context)
            time.sleep(time_to_sleep / 1000.0)
            retries += 1
        if final_exception:
            raise final_exception

    @property
    def on_connect(self):
        return self._on_connect

    @on_connect.setter
    def on_connect(self, func):
        with self._callback_mutex:
            self._on_connect = func

    @property
    def on_events_message(self):
        return self._on_events_message

    @on_events_message.setter
    def on_events_message(self, func):
        with self._callback_mutex:
            self._on_events_message = func

    @property
    def on_fatal_error(self):
        """Callback ``on_fatal_error(client, response)`` invoked on an
        ``authError`` or ``subscribeExpired`` frame.

        Return True to keep reconnecting with backoff, e.g. when the
        subscription of the same app key is going to be renewed. Any other
        return value (the default when no callback is set) stops the
        subscription and makes ``do_subscribe`` raise ``ServerException``.
        """
        return self._on_fatal_error

    @on_fatal_error.setter
    def on_fatal_error(self, func):
        with self._callback_mutex:
            self._on_fatal_error = func

    @property
    def on_log(self):
        return self._on_log

    @on_log.setter
    def on_log(self, func):
        self._on_log = func

    def _easy_log(self, level, fmt, *args):
        if self.on_log is not None:
            buf = fmt % args
            try:
                self.on_log(level, buf)
            except Exception:
                pass
        if self._logger is not None:
            self._logger.log(level, fmt, *args)

    def enable_logger(self, logger=None):
        if logger is None:
            if self._logger is not None:
                return
            logger = logging.getLogger(__name__)
        self._logger = logger

    def disable_logger(self):
        self._logger = None

    def _handle_subscribe_success(self, response):
        self._stream_subscribed = True
        self._easy_log(
            logging.INFO, "subscribe success, response:%s", response)
        with self._callback_mutex:
            on_connect = self.on_connect
        if not on_connect:
            return
        with self._in_callback_mutex:
            try:
                on_connect(self, response.payload, response)
            except Exception as err:
                self._easy_log(
                    logging.ERROR, 'Caught exception in on_connect: %s', err)
                raise err

    def _handle_fatal_error(self, response):
        """Ask ``on_fatal_error`` whether to keep reconnecting.

        Returns:
            True to keep reconnecting, False to stop the subscription.
        """
        with self._callback_mutex:
            on_fatal_error = self.on_fatal_error
        if not on_fatal_error:
            return False
        with self._in_callback_mutex:
            try:
                return on_fatal_error(self, response) is True
            except Exception as err:
                self._easy_log(
                    logging.ERROR, 'Caught exception in on_fatal_error: %s', err)
                return False

    def _handle_default(self, response, level):
        self._easy_log(level, "response:%s", response)

    def _handle_message(self, response):
        self._easy_log(
            logging.DEBUG, "message received, response:%s", response)
        with self._callback_mutex:
            on_events_message = self.on_events_message
        if not on_events_message:
            return
        with self._in_callback_mutex:
            content_type = response.contentType
            _payload = response.payload
            if JSON == content_type:
                try:
                    _payload = json.loads(response.payload)
                except Exception as err:
                    self._easy_log(
                        logging.ERROR, 'Caught exception in decode message: %s, %s', _payload, err)
                    raise err
            try:
                on_events_message(response.eventType,
                                  response.subscribeType, _payload, response)
            except Exception as err:
                self._easy_log(
                    logging.ERROR, 'Caught exception in on_events_message: %s', err)
                raise err

    def _easy_handler(self, event, data):
        try:
            response = SseSubscribeResponse(event, data)
        except ValueError as err:
            self._easy_log(
                logging.ERROR, 'Caught exception in decode sse frame: %s, %s, %s', event, data, err)
            return
        # Dispatch on the SSE frame name, the eventType value in the data is
        # the upstream business type for "event" frames only.
        if event == EVENT_BUSINESS:
            self._handle_message(response)
        elif event == EVENT_SUBSCRIBE_SUCCESS:
            self._handle_subscribe_success(response)
        elif event == EVENT_PING:
            self._handle_default(response, logging.DEBUG)
        elif event == EVENT_AUTH_ERROR or event == EVENT_SUBSCRIBE_EXPIRED:
            self._handle_default(response, logging.FATAL)
            self._fatal_response = response
        elif event == EVENT_NUM_OF_CONN_EXCEED:
            # Rejected by the session mutex, retried with backoff.
            self._handle_default(response, logging.ERROR)
            self._fatal_response = response
        else:
            self._easy_log(logging.WARNING, "unknown sse frame ignored, response:%s", response)

    @staticmethod
    def _validate_accounts(accounts):
        # A plain string is iterable too, reject it explicitly instead of
        # subscribing each character as an account ID.
        if not isinstance(accounts, (list, tuple)) or not accounts:
            raise ClientException(error_code.SDK_INVALID_PARAMETER,
                                  "accounts should be a non empty list of account IDs.")
        for account in accounts:
            if not isinstance(account, str) or not account.strip():
                raise ClientException(error_code.SDK_INVALID_PARAMETER,
                                      "account ID should be a non empty string.")

    def do_subscribe(self, accounts):
        """Subscribe the given accounts and keep reading events until stopped.

        This call is synchronous, it returns only when the retry policy gives
        up, and raises the last failure in that case.

        Args:
            accounts: non empty list of account IDs to subscribe.

        Raises:
            ClientException: ``accounts`` is empty or contains an invalid ID,
                the server would reject the request with HTTP 400.
        """
        self._validate_accounts(accounts)
        self._easy_log(logging.INFO,
                       "sse subscribe starting, url:%s, tls_enable:%s, accounts:%s",
                       self._get_url(), self._tls_enable, accounts)
        with httpx.Client(http2=True, verify=self._get_verify_value()) as session:
            self._stream_processing(session, accounts)
