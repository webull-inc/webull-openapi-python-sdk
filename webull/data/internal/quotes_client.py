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

import logging
import sys
import threading
import time
import uuid
from logging.handlers import TimedRotatingFileHandler

import paho.mqtt.client as mqttc

import webull.core.exception.error_code as error_code
from webull.core.client import ApiClient
from webull.core.common import api_type
from webull.core.endpoint.default_endpoint_resolver import DefaultEndpointResolver
from webull.core.endpoint.resolver_endpoint_request import ResolveEndpointRequest
from webull.core.exception.exceptions import ClientException
from webull.core.http.initializer.client_initializer import ClientInitializer
from webull.core.retry.retry_condition import RetryCondition
from webull.data.common.connect_ack import ConnectAck
from webull.data.internal.default_retry_policy import DefaultQuotesRetryPolicy, QuotesRetryPolicyContext
from webull.data.internal.exceptions import ConnectException, LoopException
from webull.data.internal.quotes_decoder import QuotesDecoder

DEFAULT_REGION_ID = "us"

LOG_INFO = mqttc.MQTT_LOG_INFO
LOG_NOTICE = mqttc.MQTT_LOG_NOTICE
LOG_WARNING = mqttc.MQTT_LOG_WARNING
LOG_ERR = mqttc.MQTT_LOG_ERR
LOG_DEBUG = mqttc.MQTT_LOG_DEBUG

logger = logging.getLogger(__name__)

class QuotesClient(mqttc.Client):
    LOG_FORMAT = '%(thread)d %(threadName)s %(asctime)s %(name)s %(levelname)s %(message)s'
    def __init__(self, app_key, app_secret, region_id, session_id,
                 http_host=None,
                 mqtt_host=None,
                 mqtt_port=1883,
                 tls_enable=True,
                 transport="tcp",
                 retry_policy=None,
                 downgrade_message=None):
        self._endpoint_resolver = DefaultEndpointResolver(self)
        self._client_id = session_id
        self._app_key = app_key
        self._app_secret = app_secret
        self._region_id = region_id
        self._out_api_message_mutex = threading.Lock()
        self._quotes_session_id = session_id
        self._quotes_subscribe = None
        self._quotes_unsubscribe = None
        self._on_quotes_message = None
        self._http_host = http_host
        self._mqtt_host = mqtt_host
        self._mqtt_port = mqtt_port
        self._quotes_decoder = QuotesDecoder()

        api_client = ApiClient(app_key, app_secret, region_id)
        if http_host:
            api_client.add_endpoint(region_id, http_host)
        self._api_client = api_client

        def _quotes_message(client, userdata, message):
            decoded = client._quotes_decoder.decode(message)
            if decoded:
                client._easy_log(
                    LOG_DEBUG, 'decoded message topic: %s, payload: %s', decoded[0], decoded[1])
                _on_quotes_message = client._on_quotes_message
                no_callback_topic = ['echo','notice']
                if _on_quotes_message and decoded[0] not in no_callback_topic:
                    _on_quotes_message(client, decoded[0], decoded[1])
            else:
                client._easy_log(
                    LOG_ERR, 'unexpected decoding for message topic: %s', message.topic)

        def _quotes_on_connect(client, userdata, flags, rc):
            if rc == 0:
                with self._callback_mutex:
                    _quotes_subscribe = self._quotes_subscribe
                if _quotes_subscribe:
                    with self._out_api_message_mutex:
                        try:
                            _quotes_subscribe(
                                client, self._api_client, self._quotes_session_id)
                        except Exception as e:
                            self._easy_log(
                                LOG_ERR, 'Caught exception in on_quotes_subscribe: %s', e)
                            raise
                else:
                    raise ClientException(
                        error_code.SDK_INVALID_PARAMETER, "on_quotes_subscribe func must be set")
            else:
                error_msg = ''
                ack = ConnectAck.from_code(rc)
                if ack is not None:
                    error_msg = ack.value[1]
                raise ConnectException(rc, error_msg)

        self._quotes_message = _quotes_message
        self._quotes_on_connect = _quotes_on_connect
        mqttc.Client.__init__(self, self._client_id, transport=transport, reconnect_on_failure=False)
        self.username_pw_set(self._app_key, uuid.uuid4().hex)
        if tls_enable:
            self.tls_set()
        if retry_policy:
            self._retry_policy = retry_policy
        else:
            self._retry_policy = DefaultQuotesRetryPolicy()
        self._mqtt_host = mqtt_host

    @property
    def on_quotes_subscribe(self):
        return self._quotes_subscribe

    @on_quotes_subscribe.setter
    def on_quotes_subscribe(self, func):
        with self._callback_mutex:
            self._quotes_subscribe = func

    @property
    def on_quotes_unsubscribe(self):
        return self._quotes_unsubscribe

    @on_quotes_unsubscribe.setter
    def on_quotes_unsubscribe(self, func):
        with self._callback_mutex:
            self._quotes_unsubscribe = func

    @property
    def quotes_session_id(self):
        return self._quotes_session_id

    @property
    def api_client(self):
        return self._api_client

    @property
    def on_quotes_message(self):
        return self._on_quotes_message

    @on_quotes_message.setter
    def on_quotes_message(self, func):
        with self._callback_mutex:
            self._on_quotes_message = func

    def register_payload_decoder(self, type, decoder):
        with self._callback_mutex:
            self._quotes_decoder.register_payload_decoder(type, decoder)

    def _quotes_connect(self, host, port):
        self.on_message = self._quotes_message
        self.on_connect = self._quotes_on_connect
        if not host:
            endpoint_request = ResolveEndpointRequest(
                self._region_id, api_type=api_type.QUOTES)
            endpoint = self._endpoint_resolver.resolve(endpoint_request)
            _host = endpoint
        else:
            _host = host
        try:
            return super().connect(_host, port)
        except Exception as e:
            self._easy_log(
                LOG_ERR, 'Caught exception in connect: %s, host: %s, port: %s, ssl: %s', e, _host, port, self._ssl)
            raise e

    def connect_and_loop_forever(self, timeout=1, logger_enable=True, customer_logger=None):
        self._init_logger(logger_enable, customer_logger)
        self._init_client()
        retry_policy_context = QuotesRetryPolicyContext(None, 0, None)
        retries = 0
        final_exception = None
        while True:
            if self._thread_terminate is True:
                self._easy_log(LOG_WARNING,
                               'exited due to thread terminated')
                self._sock_close()
                return
            try:
                self._quotes_connect(self._mqtt_host, self._mqtt_port)
                loop_ret = super().loop_forever(timeout)
                # loop_ret != 0 means unexpected error returned from server, should be retry in future
                if loop_ret != 0:
                    raise LoopException(loop_ret)
                else:
                    self._easy_log(LOG_WARNING, 'exited normally')
                    return
            except ConnectException as connect_exception:
                final_exception = connect_exception
                retry_policy_context = QuotesRetryPolicyContext(
                    None, retries, connect_exception.error_code)
                self._easy_log(LOG_ERR,
                               'connect exception:%s', connect_exception)
            except Exception as exception:
                final_exception = exception
                retry_policy_context = QuotesRetryPolicyContext(
                    exception, retries, None)
                self._easy_log(LOG_ERR, 'exception:%s', exception)
            retryable = self._retry_policy.should_retry(retry_policy_context)
            if retryable & RetryCondition.NO_RETRY:
                self._easy_log(
                    LOG_ERR, 'processing will stopped due to not be retryable, retry_context:%s', retry_policy_context)
                break
            retry_policy_context.retryable = retryable
            time_to_sleep = self._retry_policy.compute_delay_before_next_retry(
                retry_policy_context)
            self._easy_log(LOG_INFO, "next retry will be started in %s ms, retry_context:%s",
                           time_to_sleep, retry_policy_context)
            time.sleep(time_to_sleep / 1000.0)
            retries += 1
            retry_policy_context.retries_attempted = retries
        self._sock_close()
        if final_exception:
            raise final_exception

    def connect_and_loop_async(self, timeout=1, thread_daemon=False, logger_enable=True, customer_logger=None):
        if self._thread is not None:
            return mqttc.MQTT_ERR_INVAL
        self._sockpairR, self._sockpairW = mqttc._socketpair_compat()
        self._thread_terminate = False
        self._thread = threading.Thread(
            target=self.connect_and_loop_forever, name="Thread-Async-Quotes-Client", args=(timeout,))
        self._thread.daemon = True
        self._thread.daemon = thread_daemon
        self._thread.start()

    def connect_and_loop_start(self, timeout=1, logger_enable=True, customer_logger=None):
        self.connect_and_loop_async(timeout, True, logger_enable, customer_logger)

    def loop_wait(self):
        if self._thread is None:
            return mqttc.MQTT_ERR_INVAL
        if threading.current_thread() != self._thread:
            self._thread.join()

    def loop_stop(self):
        return super().loop_stop()

    def set_stream_logger(self, log_level=logging.DEBUG, logger_name='webull.data', stream=None,
                          format_string=None):
        if format_string is None:
            format_string = self.LOG_FORMAT

        # http
        self.api_client.set_stream_logger(log_level, 'webull.core', stream, format_string)

        # mqtt
        log = logging.getLogger(logger_name)
        log.setLevel(log_level)
        ch = logging.StreamHandler(stream)
        ch.setLevel(log_level)
        formatter = logging.Formatter(format_string)
        ch.setFormatter(formatter)
        log.addHandler(ch)

    def set_file_logger(self, path, log_level=logging.DEBUG, logger_name='webull.data', format_string=None, when='H', interval=1, backup_count=72):
        if format_string is None:
            format_string = self.LOG_FORMAT

        # http
        self.api_client.set_file_logger(path, log_level, 'webull.core', format_string, when, interval, backup_count)

        # mqtt
        log = logging.getLogger(logger_name)
        log.setLevel(log_level)
        handler = TimedRotatingFileHandler(
            filename=path,
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding='utf-8'
        )
        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)
        log.addHandler(handler)

    def _init_logger(self, logger_enable=True, customer_logger=None):

        if logger_enable is not True:
            return

        if customer_logger:
            customer_api_logger = logging.getLogger("webull.core")
            customer_api_logger.setLevel(customer_logger.level)
            for handler in customer_logger.handlers:
                customer_api_logger.addHandler(handler)
            self.api_client.set_logger(customer_api_logger)
            self.enable_logger(customer_logger)
        else:
            log_format = '%(thread)d %(asctime)s %(name)s %(levelname)s %(message)s'
            log_file_path = 'webull_data_streaming_sdk.log'
            self.set_stream_logger(stream=sys.stdout, logger_name='webull.data', log_level=logging.INFO, format_string=log_format)
            self.set_file_logger(path=log_file_path, logger_name='webull.data', log_level=logging.INFO, format_string=log_format)
            self.enable_logger(logging.getLogger('webull.data'))


    def _init_client(self):
            ClientInitializer.initializer(self.api_client)
