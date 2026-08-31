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

from webull.data.internal.quotes_payload_decoder import BaseQuotesPayloadDecoder


class NoticeDecoder(BaseQuotesPayloadDecoder):
    """Decoder for notice messages from the server.

    Notice messages are JSON-encoded and include:
    - type '1001': status message with rtt, drop, sent fields
    - type '1002': permission preemption with content field
    """

    def __init__(self):
        super().__init__()

    def parse(self, payload):
        return json.loads(payload.decode("utf-8"))
