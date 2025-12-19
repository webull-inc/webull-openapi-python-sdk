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
import uuid
from time import sleep

from webull.core.client import ApiClient
from webull.data.common.category import Category
from webull.trade.trade_client import TradeClient

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"
account_id = "<your_account_id>"
# The token_dir parameter can be used to specify the directory for storing the 2FA token. Both absolute and relative paths are supported and this option has the highest priority.
# Alternatively, the storage directory can be configured via an environment variable with the key WEBULL_OPENAPI_TOKEN_DIR, which also supports both absolute and relative paths.
# If neither is specified, the default configuration will be used, and the token will be stored at conf/token.txt under the current working directory.
# token_dir = "<your_token_dir>"
# api_client.set_token_dir(token_dir)

api_client = ApiClient(your_app_key, your_app_secret, region_id)
api_client.add_endpoint(region_id, optional_api_endpoint)


if __name__ == '__main__':
    trade_client = TradeClient(api_client)

    res = trade_client.account.get_app_subscriptions()
    if res.status_code == 200:
        print('app subscriptions:', res.json())

    res = trade_client.account.get_account_profile(account_id)
    if res.status_code == 200:
        print('account profile:', res.json())

    res = trade_client.account.get_account_position(account_id)
    if res.status_code == 200:
        print('account position:', res.json())

    res = trade_client.account.get_account_balance(account_id, 'HKD')
    if res.status_code == 200:
        print('account balance:', res.json())

    client_order_id = uuid.uuid4().hex
    print('client order id:', client_order_id)
    stock_order = {
        "account_id": account_id,
        "stock_order": {
            "client_order_id": client_order_id,
            "instrument_id": "913256135",
            "side": "BUY",
            "tif": "DAY",
            "order_type": "MARKET",
            "qty": "1",
            "extended_hours_trading": False
        }
    }

    # This is an optional feature; you can still make a request without setting it.
    custom_headers_map = {"category": Category.US_STOCK.name}
    trade_client.order.add_custom_headers(custom_headers_map)
    res = trade_client.order.place_order_v2(stock_order['account_id'], stock_order['stock_order'])
    trade_client.order.remove_custom_headers()
    if res.status_code == 200:
        print('place order v2 res:', res.json())

    res = trade_client.order.replace_order_v2(stock_order['account_id'], stock_order['stock_order'])
    if res.status_code == 200:
        print('replace order v2 res:', res.json())

    res = trade_client.order.list_open_orders(account_id, page_size=20)
    if res.status_code == 200:
        print('open orders:', res.json())

    res = trade_client.order.list_today_orders(account_id, page_size=20)
    if res.status_code == 200:
        print('today orders', res.json())

    res = trade_client.order.query_order_detail(account_id, client_order_id)
    if res.status_code == 200:
        print('order detail:', res.json())

    res = trade_client.order.cancel_order(account_id, client_order_id)
    if res.status_code == 200:
        print('cancel order status:', res.json())



    # Options
    # For option order inquiries, please use the V2 query interface: api.order_v2.get_order_detail(account_id, client_order_id).
    client_order_id = uuid.uuid4().hex
    option_new_orders = [
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

    # preview
    res = trade_client.order.preview_option(account_id, option_new_orders)
    if res.status_code == 200:
        print("preview option=" + json.dumps(res.json(), indent=4))
    sleep(5)

    # place
    # This is an optional feature; you can still make a request without setting it.
    custom_headers_map = {"category": Category.US_OPTION.name}
    trade_client.order.add_custom_headers(custom_headers_map)
    res = trade_client.order.place_option(account_id, option_new_orders)
    trade_client.order.remove_custom_headers()
    if res.status_code == 200:
        print("place option=" + json.dumps(res.json(), indent=4))
    sleep(5)

    # replace
    option_modify_orders = [
        {
            "client_order_id": client_order_id,
            "quantity": "2",
            "limit_price": "11.3",
            "orders": [
                {
                    "client_order_id": client_order_id,
                    "quantity": "2"
                }
            ]
        }
    ]
    res = trade_client.order.replace_option(account_id, option_modify_orders)
    if res.status_code == 200:
        print("replace option=" + json.dumps(res.json(), indent=4))
    sleep(5)

    # cancel
    res = trade_client.order.cancel_option(account_id, client_order_id)
    if res.status_code == 200:
        print("cancel option=" + json.dumps(res.json(), indent=4))
