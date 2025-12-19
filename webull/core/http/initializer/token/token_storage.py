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
import os
import platform
import re
from pathlib import Path

from webull.core.exception.exceptions import ClientException

logger = logging.getLogger(__name__)

class TokenStorage:

    DEFAULT_TOKEN_PATH = "conf"
    DEFAULT_TOKEN_FILE = "token.txt"
    DEFAULT_ENV_TOKEN_DIR = "WEBULL_OPENAPI_TOKEN_DIR"

    _INVALID_CHARS = {
        "windows": re.compile(r'[<>"|?*]'),
        "posix": re.compile(r'[\0]')
    }

    def __init__(self, custom_token_dir=None):
        # Resolve the final storage directory (priority: custom direction > environment variable > default).
        self.storage_token_dir = self._resolve_dir(custom_token_dir)
        # Full path validation
        self._validate_path()
        # Ensure the directory exists
        self._ensure_dir_exists()
        # Full path
        self.token_file = self.storage_token_dir / self.DEFAULT_TOKEN_FILE
        logger.info("storage_token initialized path:%s.",self.token_file)
        # Check file exists
        self._check_file_exists()

    def _resolve_dir(self, custom_token_dir=None) -> Path:
        if custom_token_dir and custom_token_dir.strip():
            # custom direction
            raw_dir = custom_token_dir.strip()
            logger.info("storage_token uses the custom configuration, token_dir:%s.", raw_dir)
        elif env_dir := os.getenv(self.DEFAULT_ENV_TOKEN_DIR):
            # environment variable
            raw_dir = env_dir.strip()
            logger.info("storage_token uses environment variable configuration, %s:%s.", self.DEFAULT_ENV_TOKEN_DIR, raw_dir)
        else:
            # default
            raw_dir = self.DEFAULT_TOKEN_PATH
            logger.info("storage_token uses the default configuration, %s.", raw_dir)

        # Resolve path
        normalized_token_dir = Path(raw_dir).expanduser().absolute()
        return normalized_token_dir

    def _validate_path(self):

        dir_path = self.storage_token_dir
        os_type = platform.system().lower()

        self._validate_path_syntax(dir_path, os_type)
        self._validate_path_access(dir_path)

    def _validate_path_syntax(self, path: Path, os_type: str):
        """Syntax validity check"""
        invalid_pattern = self._INVALID_CHARS["windows"] if "windows" in os_type else self._INVALID_CHARS["posix"]
        if invalid_pattern.search(str(path)):
            msg = ("storage_token path contains illegal characters, path:%s." % (str(path)))
            logger.warning(msg)

    def _validate_path_access(self, path: Path):
        """Accessibility/permission check"""
        if path.exists():
            if not path.is_dir():
                msg = ("storage_token path already exists but is not a directory, path:%s." % (str(path)))
                logger.warning(msg)
                return
            if not os.access(path, os.R_OK | os.W_OK):
                msg = ("storage_token directory has no read/write permission. Please check the configuration, path:%s." % (str(path)))
                logger.warning(msg)
        else:
            parent_dir = path.parent
            if not parent_dir.exists():
                msg = ("storage_token parent directory does not exist, unable to create directory. Please check the configuration, parent path:%s." % (str(parent_dir)))
                logger.warning(msg)
                return
            if not os.access(parent_dir, os.R_OK | os.W_OK | os.X_OK):
                msg = ("storage_token parent directory has no read/write permission. Please check the configuration, parent path:%s." % (str(parent_dir)))
                logger.warning(msg)

    def _ensure_dir_exists(self):
        """Ensure the directory exists"""
        try:
            self.storage_token_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            msg = ("storage_token failed to create directory, file:%s." % (str(self.storage_token_dir)))
            logger.error(msg)
            raise ClientException("ERROR_STORAGE_TOKEN", str(e)) from e

    def _check_file_exists(self):
        """Check file exists"""
        full_path = Path(self.token_file)
        if full_path.is_file():
            msg = ("storage_token Note: The token file already exists, the latest token configuration will be overwritten and written to the token file after successful 2FA verification. path:%s." % self.token_file)
            logger.warning(msg)

    def get_token_file_path(self):
        return self.token_file