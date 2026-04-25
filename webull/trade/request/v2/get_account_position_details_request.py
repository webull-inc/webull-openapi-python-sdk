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
from webull.core.request import ApiRequest


class AccountPositionDetailsRequest(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/openapi/assets/position/details", version='v2', method="GET", query_params={})

    def set_account_id(self, account_id):
        self.add_query_param("account_id", account_id)

    def set_instrument_id(self, instrument_id):
        self.add_query_param("instrument_id", instrument_id)

    def set_page_size(self, page_size):
        if page_size:
            self.add_query_param("page_size", page_size)

    def set_last_id(self, last_id):
        if last_id:
            self.add_query_param("last_id", last_id)