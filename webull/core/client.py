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

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
This file borrowed some of its methods from a  modified fork of the
https://github.com/aliyun/aliyun-openapi-python-sdk/blob/master/aliyun-python-sdk-core/aliyunsdkcore/client.py
which was part of Alibaba Group.
"""

import json
import logging
import platform
import time
from logging.handlers import TimedRotatingFileHandler

import webull.core
import webull.core.headers as hd
import webull.core.retry.retry_policy as retry_policy
from webull.core import compat
from webull.core.auth.signers.signer_factory import SignerFactory
from webull.core.common.api_type import DEFAULT as HTTP_API_TYPE
from webull.core.endpoint.default_endpoint_resolver import DefaultEndpointResolver
from webull.core.endpoint.resolver_endpoint_request import ResolveEndpointRequest
from webull.core.exception import error_code
from webull.core.exception.exceptions import ClientException, ServerException
from webull.core.headers import WB_USER_ID
from webull.core.http.response import Response
from webull.core.request import BaseRequest
from webull.core.retry.retry_condition import RetryCondition
from webull.core.retry.retry_policy_context import RetryPolicyContext
from webull.core.utils import common, validation
from webull.core.vendored.requests import codes
from webull.core.vendored.requests.structures import CaseInsensitiveDict
from webull.core.vendored.requests.structures import OrderedDict

DEFAULT_READ_TIMEOUT = 10
DEFAULT_CONNECTION_TIMEOUT = 5
DEFAULT_PORT = 443
DEFAULT_REGION_ID = "us"

logger = logging.getLogger(__name__)

class ApiClient:
    LOG_FORMAT = '%(thread)d %(threadName)s %(asctime)s %(name)s %(levelname)s %(message)s'
    def __init__(
        self,
        app_key,
        app_secret,
        region_id,
        user_agent=None,
        port=DEFAULT_PORT,
        connect_timeout=None,
        timeout=None,
        credential=None,
        verify=None,
        auto_retry=False,
        max_retry_num=None,
        user_id=None,
        token_check_duration_seconds = 300,
        token_check_interval_seconds = 5
    ):
        self._file_logger_set = None
        self._stream_logger_set = None
        self._app_key = app_key
        self._app_secret = app_secret
        self._region_id = region_id
        self._user_agent = user_agent
        self._port = port
        self._connect_timeout = connect_timeout
        self._read_timeout = timeout
        self._extra_user_agent = {}
        self._verify = verify
        _credential = {
            'app_key': app_key,
            'app_secret': app_secret,
            'credential': credential,
        }
        self._signer = SignerFactory.get_signer(_credential)
        self._endpoint_resolver = DefaultEndpointResolver(self) 
        self._max_retry_num = max_retry_num
        self._auto_retry = auto_retry
        self._user_id = user_id
        if self._auto_retry:
            self._retry_policy = retry_policy.get_default_retry_policy(self._max_retry_num)
        else:
            self._retry_policy = retry_policy.NO_RETRY_POLICY
        self._token = None

        validation.assert_integer_positive(token_check_duration_seconds, "token_check_duration_seconds")
        self._token_check_duration_seconds = token_check_duration_seconds
        validation.assert_integer_positive(token_check_interval_seconds, "token_check_interval_seconds")
        self._token_check_interval_seconds = token_check_interval_seconds

    def get_region_id(self):
        return self._region_id

    def get_app_key(self):
        return self._app_key 

    def get_app_secret(self):
        return self._app_secret 
    
    def get_user_agent(self):
        return self._user_agent
    
    def get_verify(self):
        return self._verify

    def set_user_id(self):
        return self._user_id

    def set_user_agent(self, agent):
        """
        User agent set to client will overwrite the request setting.
        :param agent:
        :return:
        """
        self._user_agent = agent
    
    def append_user_agent(self, key, value):
        self._extra_user_agent.update({key: value})

    def set_token(self, token):
        self._token = token

    def get_token(self):
        return self._token

    def get_token_check_duration_seconds(self):
        return self._token_check_duration_seconds

    def get_token_check_interval_seconds(self):
        return self._token_check_interval_seconds

    @staticmethod
    def user_agent_header():
        base = '%s (%s %s;%s)' \
               % ('WebullApiSDK',
                  platform.system(),
                  platform.release(),
                  platform.machine()
                  )
        return base

    @staticmethod
    def default_user_agent():
        default_agent = OrderedDict()
        default_agent['Python'] = platform.python_version()
        default_agent['Core'] = __import__('webull.core').__version__
        default_agent['python-requests'] = __import__(
            'webull.core.vendored.requests.__version__', globals(), locals(),
            ['vendored', 'requests', '__version__'], 0).__version__

        return CaseInsensitiveDict(default_agent)

    def client_user_agent(self):
        client_user_agent = {}
        if self.get_user_agent() is not None:
            client_user_agent.update({'client': self.get_user_agent()})
        else:
            client_user_agent.update(self._extra_user_agent)

        return CaseInsensitiveDict(client_user_agent)
    
    def handle_extra_agent(self, request):
        client_agent = self.client_user_agent()
        request_agent = request.request_user_agent()

        if client_agent is None:
            return request_agent

        if request_agent is None:
            return client_agent
        for key in request_agent:
            if key in client_agent:
                client_agent.pop(key)
        client_agent.update(request_agent)
        return client_agent

    @staticmethod
    def merge_user_agent(default_agent, extra_agent):
        if default_agent is None:
            return extra_agent

        if extra_agent is None:
            return default_agent
        user_agent = default_agent.copy()
        for key, value in extra_agent.items():
            if key not in default_agent:
                user_agent[key] = value
        return user_agent 

    def get_port(self):
        return self._port
    
    def _compose_ua(self, request):
        ua_base = self.user_agent_header()
        extra_ua = self.handle_extra_agent(request)
        default_ua = self.default_user_agent() 
        ua = self.merge_user_agent(default_ua, extra_ua)
        for k, v in ua.items():
            ua_base += ' %s/%s' % (k, v) 
        return ua_base
    
    def _make_http_response(self, endpoint, request, read_timeout, connect_timeout, specific_signer=None):
        body_params = request.get_body_params()
        body = None
        if body_params is not None:
            body = common.json_dumps_compact(body_params)
            request.set_content(body)
        method = request.get_method()
        signer = self._signer if specific_signer is None else specific_signer
        request.set_endpoint(endpoint)
        headers = signer.sign(request) 
        headers['User-Agent'] = self._compose_ua(request)
        if self.get_token():
            headers['x-access-token'] = self.get_token()

        protocol = request.get_protocol_type()
        url = request.get_url()
        response = Response(
            endpoint,
            url,
            method,
            headers,
            protocol,
            request.get_content(),
            self._port,
            read_timeout=read_timeout,
            connect_timeout=connect_timeout,
            verify=self.get_verify())
        response.set_content(body, "utf-8")
        return response
    
    def _implementation_of_do_action(self, request, signer=None):
        if not isinstance(request, BaseRequest):
            raise ClientException(error_code.SDK_INVALID_REQUEST)
        request.add_header('Accept-Encoding', 'gzip')

        if self._user_id:
            request.add_header(WB_USER_ID, self._user_id)

        if request.endpoint:
            endpoint = request.endpoint
        else:
            endpoint = self._resolve_endpoint(request)
        return self._handle_retry_and_timeout(endpoint, request, signer)

    def _handle_retry_and_timeout(self, endpoint, request, signer):
        retry_policy_context = RetryPolicyContext(request, None, 0, None)
        request_read_timeout = self._get_request_read_timeout(request)
        request_connect_timeout = self._get_request_connect_timeout(request)
        retries = 0
        while True:
           status, headers, body, exception, response = \
           self._handle_single_request(endpoint, request, request_read_timeout, request_connect_timeout, signer)
           retry_policy_context = RetryPolicyContext(request, exception, retries, status)
           retryable = self._retry_policy.should_retry(retry_policy_context)
           if retryable & RetryCondition.NO_RETRY:
               break
           logger.debug("Retry needed. Request:%s Retries:%d", request.get_action_name(), retries)
           retry_policy_context.retryable = retryable
           time_to_sleep = self._retry_policy.compute_delay_before_next_retry(retry_policy_context)
           time.sleep(time_to_sleep / 1000.0)
           retries += 1

        if isinstance(exception, ClientException):
            raise exception
        return status, headers, body, exception, response
    
    def _handle_single_request(self, endpoint, request, read_timeout, connect_timeout, signer):
        http_response = self._make_http_response(endpoint, request, read_timeout, connect_timeout, signer)
        try:
            status, headers, body, response = http_response.get_response_object()
        except IOError as e:
            exception = ClientException(error_code.SDK_HTTP_ERROR, compat.ensure_string('%s' % e))
            msg = "HttpError occurred. Host:%s SDK-Version:%s Request:%s ClientException:%s" % (
                         endpoint, webull.core.__version__, json.dumps(vars(request), default=str, indent=2), exception)
            logger.error(compat.ensure_string(msg))
            return None, None, None, exception, None
        exception = self._get_server_exception(request, status, headers, body, endpoint, request.string_to_sign)
        return status, headers, body, exception, response
    
    @staticmethod
    def _parse_error_info_from_response_body(body_obj):
        error_code_to_return = error_code.SDK_UNKNOWN_SERVER_ERROR
        error_msg_to_return = ""
        if body_obj and body_obj.get('error_code'):
            error_code_to_return = body_obj.get('error_code')
        if body_obj and body_obj.get('message'):    
            error_msg_to_return = body_obj.get('message')
        return error_code_to_return, error_msg_to_return
    
    def _get_server_exception(self, request, http_status, headers, response_body, endpoint, string_to_sign):
        request_id = headers.get(hd.REQUEST_ID)
        body_obj = None
        try:
            if response_body:
                response_content = response_body.decode('utf-8')
                if response_content:
                    body_obj = json.loads(response_body.decode('utf-8'))
        except (ValueError, TypeError, AttributeError):
            logger.warning('Failed to parse response as json format, Request:%s response:%s, request_id:%s',
                           json.dumps(vars(request), default=str, indent=2), response_body, request_id)
        if http_status < codes.OK or http_status >= codes.MULTIPLE_CHOICES:
            server_error_code, server_error_msg = self._parse_error_info_from_response_body(body_obj)
            exception = ServerException(server_error_code, server_error_msg, http_status, request_id)
            msg = "ServerException occurred. Host:%s SDK-Version:%s Request:%s Response:%s ServerException:%s" % (
                         endpoint, webull.core.__version__, json.dumps(vars(request), default=str, indent=2), body_obj, exception)
            logger.error(compat.ensure_string(msg))
            return exception

    def _get_request_read_timeout(self, request):
        # TODO: replace it with a timeout_handler
        if request._request_read_timeout:
            return request._request_read_timeout
        if self._read_timeout:
            return self._read_timeout
        return DEFAULT_READ_TIMEOUT
         
    def _get_request_connect_timeout(self, request):
        if request._request_connect_timeout:
            return request._request_connect_timeout
        if self._connect_timeout:
            return self._connect_timeout
        return DEFAULT_CONNECTION_TIMEOUT
    
    def _resolve_endpoint(self, request):
        resolve_request = ResolveEndpointRequest(
            self._region_id
        )
        return self._endpoint_resolver.resolve(resolve_request)
    
    def add_endpoint(self, region_id, endpoint, api_type=HTTP_API_TYPE):
        self._endpoint_resolver.put_endpoint_entry(region_id, api_type, endpoint)

    def set_logger(self, custom_logger):
        global logger
        logger = custom_logger

    def set_stream_logger(self, log_level=logging.DEBUG, logger_name='webull.core', stream=None,
                          format_string=None):
        log = logging.getLogger(logger_name)
        log.setLevel(log_level)
        ch = logging.StreamHandler(stream)
        ch.setLevel(log_level)
        if format_string is None:
            format_string = self.LOG_FORMAT
        formatter = logging.Formatter(format_string)
        ch.setFormatter(formatter)
        log.addHandler(ch)
        self._stream_logger_set = True

    def set_file_logger(self, path, log_level=logging.DEBUG, logger_name='webull.core', format_string=None, when='H', interval=1, backup_count=72):
        log = logging.getLogger(logger_name)
        log.setLevel(log_level)
        handler = TimedRotatingFileHandler(
            filename=path,
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding='utf-8'
        )

        if format_string is None:
            format_string = self.LOG_FORMAT
        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)
        log.addHandler(handler)
        self._file_logger_set = True

    def get_response(self, api_request):
        status, headers, body, exception, response = self._implementation_of_do_action(api_request)
        if exception:
            logger.error("get_response exception. %s", json.dumps(vars(exception), default=str, indent=2))
            raise exception
        logger.debug('Response received, status:%s, headers:%s, body:%s' % (status, headers, body))
        return response
