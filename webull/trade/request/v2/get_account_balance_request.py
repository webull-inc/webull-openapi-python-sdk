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


class AccountBalanceRequest(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/openapi/account/balance", version='v2', method="GET", query_params={})

    def set_account_id(self, account_id):
        self.add_query_param("account_id", account_id)

    def set_total_asset_currency(self, total_asset_currency="HKD"):
        self.add_query_param("total_asset_currency", total_asset_currency)
        