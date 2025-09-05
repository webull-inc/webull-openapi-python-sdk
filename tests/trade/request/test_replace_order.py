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

import unittest

from webull.core.client import ApiClient
from webull.core.exception.exceptions import ServerException
from webull.core.http.initializer.client_initializer import ClientInitializer
from webull.trade.request.replace_order_request import ReplaceOrderRequest


optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"
account_id = "<your_account_id>"
api_client = ApiClient(your_app_key, your_app_secret, region_id)
api_client.add_endpoint(region_id, optional_api_endpoint)
ClientInitializer.initializer(api_client)

stock_order = {
    "account_id": "ULGALPNJ7QMN0MP38UFM2PMN9A",
    "stock_order": {
        "client_order_id": "0191646207512192",
        "instrument_id": "913256409",
        "side": "BUY",
        "tif": "DAY",
        "order_type": "ENHANCED_LIMIT",
        "limit_price": "386.000",
        "qty": "200",
        "extended_hours_trading": False
    }
}


class TestOrderOperation(unittest.TestCase):
    def test_replace_order(self):
        request = ReplaceOrderRequest()
        request.set_endpoint(optional_api_endpoint)
        request.set_account_id(stock_order['account_id'])
        request.set_client_order_id(stock_order['stock_order']['client_order_id'])
        request.set_side(stock_order['stock_order']['side'])
        request.set_tif(stock_order['stock_order']['tif'])
        request.set_instrument_id(stock_order['stock_order']['instrument_id'])
        request.set_order_type(stock_order['stock_order']['order_type'])
        request.set_limit_price(stock_order['stock_order']['limit_price'])
        request.set_qty(stock_order['stock_order']['qty'])
        request.set_extended_hours_trading(stock_order['stock_order']['extended_hours_trading'])
        post_body = request.get_body_params()
        print(post_body)
        params = request.get_query_params()
        print(params)
        try:
            response = api_client.get_response(request)
            print(response.json())

        except ServerException as se:
            print(se.get_error_code(), ":", se.get_error_msg())