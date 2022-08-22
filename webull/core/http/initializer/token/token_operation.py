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

# coding=utf-8

import logging

from webull.core.http.initializer.token.bean.check_token_request import CheckTokenRequest
from webull.core.http.initializer.token.bean.create_token_request import CreateTokenRequest
from webull.core.http.initializer.token.bean.refresh_token_request import RefreshTokenRequest


class TokenOperation:
    def __init__(self, api_client):
        self.client = api_client

    def create_token(self, token):
        """
        Create a token
        """
        create_token_request = CreateTokenRequest()
        create_token_request.set_token(token)
        response = self.client.get_response(create_token_request)
        return response

    def check_token(self, token):
        """
        Check whether the token is verified
        """
        check_token_request = CheckTokenRequest()
        check_token_request.set_token(token)
        response = self.client.get_response(check_token_request)
        return response

    def refresh_token(self, token):
        """
        Refresh token
        """
        refresh_token_request = RefreshTokenRequest()
        refresh_token_request.set_token(token)
        response = self.client.get_response(refresh_token_request)
        return response