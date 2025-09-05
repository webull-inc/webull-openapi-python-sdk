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
import unittest
import uuid

from webull.core.client import ApiClient
from webull.core.exception.exceptions import ServerException
from webull.core.http.initializer.client_initializer import ClientInitializer
from webull.data.common.category import Category
from webull.trade.request.v2.place_option_request import PlaceOptionRequest

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"
account_id = "<your_account_id>"
api_client = ApiClient(your_app_key, your_app_secret, region_id)
api_client.add_endpoint(region_id, optional_api_endpoint)
ClientInitializer.initializer(api_client)

client_order_id = uuid.uuid4().hex
new_orders = [
                {
                    "client_order_id": client_order_id,
                    "combo_type": "NORMAL",
                    "order_type": "LIMIT",
                    "quantity": "1",
                    "limit_price": "11.25",
                    "option_strategy": "SINGLE",
                    "side": "BUY",
                    "time_in_force": "GTC",
                    "entrust_type": "QTY",
                    "orders": [
                        {
                            "side": "BUY",
                            "quantity": "1",
                            "symbol": "AAPL",
                            "strike_price": "250.0",
                            "init_exp_date": "2025-08-15",
                            "instrument_type": "OPTION",
                            "option_type": "CALL",
                            "market": "US"
                        }
                    ]
                }
            ]


class TestOptionOperation(unittest.TestCase):
    def test_preview_order(self):
        request = PlaceOptionRequest()
        request.set_endpoint(optional_api_endpoint)
        request.set_account_id(account_id)
        request.set_new_orders(new_orders)
        post_body = request.get_body_params()
        print(json.dumps(post_body, indent=4))
        params = request.get_query_params()
        print(params)

        # This is an optional feature; you can still make a request without setting it.
        custom_headers_map = {"category": Category.US_OPTION.name}
        request.add_custom_headers(custom_headers_map)

        try:
            response = api_client.get_response(request)
            print(response.json())

        except ServerException as se:
            print(se.get_error_code(), ":", se.get_error_msg())
