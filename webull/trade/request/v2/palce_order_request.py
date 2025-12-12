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


class PlaceOrderRequest(ApiRequest):
    """
    Deprecated. Use :func:`place_order_request` instead.
    """
    def __init__(self):
        super().__init__("/openapi/trade/stock/order/place", version='v2', method="POST", body_params={})

    def set_new_orders(self, new_orders):
        self.add_body_params("new_orders", new_orders)

    def set_account_id(self, account_id):
        self.add_body_params("account_id", account_id)

    def set_client_combo_order_id(self, client_combo_order_id):
        if client_combo_order_id:
            self.add_body_params("client_combo_order_id", client_combo_order_id)

    def add_custom_headers_from_order(self, new_orders):
        if not new_orders:
            return

        if isinstance(new_orders, list) and new_orders[0]:
            first_order = new_orders[0]
            instrument_type = first_order.get("instrument_type")
            market = first_order.get("market")
            category = market + "_" + instrument_type
            if category is not None:
                self.add_header("category", category)