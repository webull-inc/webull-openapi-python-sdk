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
import time

from webull.core import compat
from webull.core.http.initializer.token.token_storage import TokenStorage
from webull.core.utils import desensitize
from webull.core.exception.exceptions import ClientException
from webull.core.http.initializer.token.bean.access_token import AccessToken
from webull.core.http.initializer.token.token_operation import TokenOperation

logger = logging.getLogger(__name__)

class TokenManager:

    def __init__(self, custom_token_dir=None):
        token_storage = TokenStorage(custom_token_dir=custom_token_dir)
        self.token_file_path = token_storage.get_token_file_path()

    def init_token(self, api_client):
        local_access_token = self.load_token_from_local()
        local_token = local_access_token.token if local_access_token else None
        server_access_token = self.fetch_token_from_server(api_client, local_token)
        self.save_token_to_local(server_access_token)

        if server_access_token.get("status") != "NORMAL":
            msg = ("init_token status not verified error. token:%s expires:%s status:%s" %
                   (desensitize.desensitize_token(server_access_token.get("token")), server_access_token.get("expires"), server_access_token.get("status")))
            logger.error(msg)
            raise ClientException("ERROR_INIT_TOKEN", msg)

        logger.info("init_token finished. token:%s expires:%s status:%s",
                    desensitize.desensitize_token(server_access_token.get("token")), server_access_token.get("expires"), server_access_token.get("status"))
        access_token = server_access_token.get("token")
        api_client.set_token(access_token)
        return access_token

    def load_token_from_local(self):
        if not self.token_file_path.exists():
            logger.info("load_token_from_local file not exists, file:%s.", self.token_file_path)
            return None
        try:
            logger.info("load_token_from_local reading token from file...")
            with open(self.token_file_path, "r", encoding="utf-8") as f:
                token = f.readline().strip()

                str_expires = f.readline().strip()
                if str_expires and str_expires.isdigit():
                    expires = int(str_expires)
                else:
                    expires = 0

                status = f.readline().strip()

            logger.info("load_token_from_local read local token result. token:%s expires:%s status:%s",
                        desensitize.desensitize_token(token), expires, status)
            return AccessToken(token=token, expires=expires, status=status)
        except Exception as e:
            logger.error("load_token_from_local failed, file:%s.", self.token_file_path, exc_info=True)
            raise ClientException("ERROR_LOAD_TOKEN") from e

    def save_token_to_local(self, server_access_token):
        try:
            logger.info("save_token_to_local writing token to local file. token:%s expires:%s status:%s",
                        desensitize.desensitize_token(server_access_token.get("token")), server_access_token.get("expires"), server_access_token.get("status"))
            self.token_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.token_file_path, "w", encoding="utf-8") as f:
                f.write(server_access_token.get("token") + "\n")
                f.write(str(server_access_token.get("expires")) + "\n")
                f.write(str(server_access_token.get("status")) + "\n")
            logger.info("save_token_to_local writing token to file completed.")
        except Exception as e:
            logger.error("save_token_to_local failed, file:%s.", self.token_file_path, exc_info=True)
            raise ClientException("ERROR_SAVE_TOKEN") from e

    def fetch_token_from_server(self, api_client, local_token ):
        token_operation = TokenOperation(api_client)

        create_access_token = self.create_token(token_operation, local_token)
        if create_access_token.get("status") == "NORMAL":
            logger.info("fetch_token_from_server create_token status is verified, no further check required, returning directly. token:%s expires:%s status:%s",
                        desensitize.desensitize_token(create_access_token.get("token")), create_access_token.get("expires"), create_access_token.get("status"))
            return create_access_token

        return self.check_token(api_client, token_operation, create_access_token)

    @staticmethod
    def create_token(token_operation, local_token):
        response = token_operation.create_token(local_token)

        if response.status_code != 200:
            msg = "fetch_token_from_server create_token returned non-200 response, raising exception. status_code:%s" % response.status_code
            logger.error(compat.ensure_string(msg))
            raise ClientException("ERROR_CREATE_TOKEN", msg)

        create_access_token = response.json()
        if not create_access_token:
            msg = "fetch_token_from_server create_token result is empty."
            logger.error(msg)
            raise ClientException("ERROR_CREATE_TOKEN", msg)

        if not create_access_token.get("token") or not create_access_token.get("expires") or create_access_token.get("status") is None:
            msg = ("fetch_token_from_server create_token result is empty. token:%s expires:%s status:%s" %
                   (desensitize.desensitize_token(create_access_token.get("token")), create_access_token.get("expires"), create_access_token.get("status")))
            logger.error(msg)
            raise ClientException("ERROR_CREATE_TOKEN", msg)

        logger.info("fetch_token_from_server create_token result. token:%s expires:%s status:%s" ,
                    desensitize.desensitize_token(create_access_token.get("token")), create_access_token.get("expires"), create_access_token.get("status"))
        return create_access_token

    @staticmethod
    def check_token(api_client, token_operation, create_access_token):
        duration_seconds = api_client.get_token_check_duration_seconds()
        wait_time = api_client.get_token_check_interval_seconds()
        start_time = time.time()
        logger.info("fetch_token_from_server started check_token loop. token:%s duration_seconds:%s interval_seconds:%s",
                    desensitize.desensitize_token(create_access_token.get("token")), duration_seconds, wait_time)

        while True:
            loop_start = time.time()
            response = token_operation.check_token(create_access_token.get("token"))

            if response.status_code != 200:
                msg = "fetch_token_from_server check_token returned non-200 response, raising exception. status_code:%s" % response.status_code
                logger.error(compat.ensure_string(msg))
                raise ClientException("ERROR_CHECK_TOKEN", msg)

            check_access_token = response.json()
            if not check_access_token:
                msg = "fetch_token_from_server check_token result is empty."
                logger.error(msg)
                raise ClientException("ERROR_CHECK_TOKEN", msg)

            logger.info("fetch_token_from_server result of current check_token loop. token:%s expires:%s status:%s",
                        desensitize.desensitize_token(check_access_token.get("token")),
                        check_access_token.get("expires"), check_access_token.get("status"))

            if not check_access_token.get("token") or not check_access_token.get("expires") or check_access_token.get(
                    "status") is None:
                msg = ("fetch_token_from_server check_token result is empty. token:%s expires:%s status:%s" %
                       (desensitize.desensitize_token(check_access_token.get("token")),
                        check_access_token.get("expires"), check_access_token.get("status")))
                logger.error(msg)
                raise ClientException("ERROR_CHECK_TOKEN", msg)
            # PENDING -> 0
            # NORMAL -> 1
            # INVALID -> 2
            # EXPIRED -> 3
            if check_access_token.get("status") == "INVALID" or check_access_token.get("status") == "EXPIRED" :
                msg = "fetch_token_from_server check_token status invalidate. status:%s" % check_access_token.get("status")
                logger.error(msg)
                raise ClientException("ERROR_CHECK_TOKEN", msg)

            if check_access_token.get("status") == "NORMAL":
                logger.info(
                    "fetch_token_from_server check_token status is verified, no further check required, returning directly. token:%s expires:%s status:%s",
                    desensitize.desensitize_token(create_access_token.get("token")), create_access_token.get("expires"),
                    create_access_token.get("status"))
                return check_access_token

            elapsed = time.time() - start_time
            curr_elapsed = time.time() - loop_start
            sleep_time = wait_time - curr_elapsed
            if elapsed >= duration_seconds:
                break

            logger.info("fetch_token_from_server status not verified, check_token loop will start, waiting %s seconds... (elapsed %ss / %ss). For more details, please visit the OpenAPI official website." % (wait_time, int(elapsed), duration_seconds))
            if sleep_time > 0:
                time.sleep(sleep_time)

        logger.warning(
            "fetch_token_from_server check_token loop completed. reached the maximum retries without passing validation, returning create_access_token. For more details, please visit the OpenAPI official website.")
        return create_access_token