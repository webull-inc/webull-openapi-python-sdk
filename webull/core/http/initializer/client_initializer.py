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

from webull.core.http.initializer.token.token_manager import TokenManager

logger = logging.getLogger(__name__)


class ClientInitializer:
    """Client initialization logic."""

    @staticmethod
    def initializer(api_client):
        """Client Initialization"""
        ClientInitializer.init_token(api_client)

    @staticmethod
    def init_token(api_client):
        """Initialize token"""
        if not ClientInitializer.check_region_token_enable(api_client):
            return

        token_manager = TokenManager()
        token_manager.init_token(api_client)

    @staticmethod
    def check_region_token_enable(api_client):
        """
        Check whether token checking is enabled in the specified region
        """
        if api_client is None:
            logger.warning("check_region_token_enable api_client is null, return False")
            return False

        if not api_client.get_region_id():
            logger.warning("check_region_token_enable region_id is null, return False")
            return False

        enable_region_ids = ["hk"]
        result = api_client.get_region_id() in enable_region_ids
        logger.info(
            "check_region_token_enable result is %s, enable regionIds is %s. current regionsId is %s",
            result, enable_region_ids, api_client.get_region_id()
        )
        return result