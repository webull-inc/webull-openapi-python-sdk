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
import json
# coding=utf-8

from webull.core.request import ApiRequest


class BatchPlaceOrderRequest(ApiRequest):
    def __init__(self):
        super().__init__("/openapi/trade/order/batch-place", version='v2', method="POST", body_params={})

    def set_account_id(self, account_id):
        self.add_body_params("account_id", account_id)

    def set_batch_orders(self, batch_orders):
        self.add_body_params("batch_orders", batch_orders)

    def add_custom_headers_from_order(self, batch_orders):
        if not batch_orders:
            return

        if isinstance(batch_orders, list) and batch_orders[0]:
            first_order = batch_orders[0]
            leg_list = first_order.get("legs")
            if leg_list is not None and isinstance(leg_list, list):
                for sub_leg in leg_list:
                    if (sub_leg and isinstance(sub_leg, dict)
                            and sub_leg.get("instrument_type") == "OPTION"):
                        instrument_type = sub_leg.get("instrument_type")
                        market = sub_leg.get("market")
                        category = market + "_" + instrument_type
                        if category is not None:
                            self.add_header("category", category)
                return

            market = first_order.get("market")
            instrument_type = first_order.get("instrument_type")
            category = market + "_" + instrument_type
            if category is not None:
                self.add_header("category", category)
