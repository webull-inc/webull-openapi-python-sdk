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

from webull.core import compat
from webull.core.exception.exceptions import ClientException
from webull.core.http.initializer.config.config_operation import ConfigOperation
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
        disable_config_region_ids = ["hk"]
        if api_client.get_region_id() in disable_config_region_ids:
            if not ClientInitializer._check_region_token_enable(api_client):
                return
        else:
            if not ClientInitializer._check_token_enable(api_client):
                return

        token_manager = TokenManager(api_client.get_token_dir())
        token_manager.init_token(api_client)

    @staticmethod
    def _check_region_token_enable(api_client):
        """
        Check whether token checking is enabled in the specified region
        """
        if api_client is None:
            logger.warning("_check_region_token_enable api_client is null, return False")
            return False

        if not api_client.get_region_id():
            logger.warning("_check_region_token_enable region_id is null, return False")
            return False

        enable_region_ids = ["hk"]
        result = api_client.get_region_id() in enable_region_ids
        logger.info(
            "_check_region_token_enable result is %s, enable regionIds is %s.",
            result, enable_region_ids
        )
        return result

    @staticmethod
    def _check_token_enable(api_client):
        """
        Check whether token checking is enabled
        """
        if api_client is None:
            logger.warning("_check_token_enable api_client is null, return False")
            return False

        config_operation = ConfigOperation(api_client)
        response = config_operation.get_config()

        if response.status_code != 200:
            msg = "_check_token_enable get_token_config returned non-200 response, raising exception. status_code:%s" % response.status_code
            logger.error(compat.ensure_string(msg))
            raise ClientException("ERROR_CHECK_TOKEN_ENABLE", msg)

        token_config = response.json()
        if not token_config:
            msg = "_check_token_enable get_token_config result is empty."
            logger.error(msg)
            raise ClientException("ERROR_CHECK_TOKEN_ENABLE", msg)

        result = token_config.get("token_check_enabled", False)
        logger.info("_check_token_enable result is %s",result)

        return result