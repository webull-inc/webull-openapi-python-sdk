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

from webull.core.common.easy_enum import EasyEnum

class ConnectAck(EasyEnum):
    CONNECTION_SUCCESS = (0, 'Connection successful')
    PROTOCOL_NOT_SUPPORTED = (1, 'Protocol not supported')
    SESSION_ID_IS_BLANK = (2, 'session_id is blank')
    AK_IS_BLANK = (3, 'AppKey is blank')
    UNKNOWN_ERROR = (100, 'Unknown error')
    INTERNAL_ERROR = (101, 'Internal error')
    CONNECTION_AUTHENTICATED = (102, 'Connection already authenticated')
    CONNECTION_AUTH_FAILED = (103, "Connection authentication failed")
    AK_INVALID = (104, "Invalid AppKey")
    CONNECTION_LIMIT_EXCEEDED = (105, "Connection limit exceeded")