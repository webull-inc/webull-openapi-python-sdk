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
from time import sleep

from webull.core.client import ApiClient
from webull.data.common.category import Category
from webull.trade.trade_client import TradeClient

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"
account_id = "<your_account_id>"
api_client = ApiClient(your_app_key, your_app_secret, region_id)
api_client.add_endpoint(region_id, optional_api_endpoint)


if __name__ == '__main__':
    trade_client = TradeClient(api_client)

    res = trade_client.account_v2.get_account_list()
    if res.status_code == 200:
        print("account_list=" + json.dumps(res.json(), indent=4))

    res = trade_client.account_v2.get_account_balance(account_id)
    if res.status_code == 200:
        print("account_balance=" + json.dumps(res.json(), indent=4))

    res = trade_client.account_v2.get_account_position(account_id)
    if res.status_code == 200:
        print("account_position=" + json.dumps(res.json(), indent=4))

    preview_orders = {
        "symbol": "AAPL",
        "instrument_type": "EQUITY",
        "market": "US",
        "order_type": "MARKET",
        "quantity": "1",
        "support_trading_session": "N",
        "side": "BUY",
        "time_in_force": "DAY",
        "entrust_type": "QTY"
    }
    res = trade_client.order_v2.preview_order(account_id=account_id, preview_orders=preview_orders)
    if res.status_code == 200:
        print("preview_res=" + json.dumps(res.json(), indent=4))

    client_order_id = uuid.uuid4().hex
    new_orders = {
        "client_order_id": client_order_id,
        "symbol": "AAPL",
        "instrument_type": "EQUITY",
        "market": "US",
        "order_type": "LIMIT",
        "limit_price": "188",
        "quantity": "1",
        "support_trading_session": "N",
        "side": "BUY",
        "time_in_force": "DAY",
        "entrust_type": "QTY",
        # "account_tax_type": "GENERAL"
        # "total_cash_amount": "100.20"
        # "sender_sub_id": "123321-lzg",
        # "no_party_ids":[
        #     {"party_id":"BNG144.666555","party_id_source":"D","party_role":"3"}
        # ]
    }

    # This is an optional feature; you can still make a request without setting it.
    custom_headers_map = {"category": Category.US_STOCK.name}
    trade_client.order_v2.add_custom_headers(custom_headers_map)
    res = trade_client.order_v2.place_order(account_id=account_id, new_orders=new_orders)
    trade_client.order_v2.remove_custom_headers()
    if res.status_code == 200:
        print("place_order_res=" + json.dumps(res.json(), indent=4))
    sleep(5)

    modify_orders = {
        "client_order_id": client_order_id,
        "quantity": "100",
        "limit_price": "200"
    }
    res = trade_client.order_v2.replace_order(account_id=account_id, modify_orders=modify_orders)
    if res.status_code == 200:
        print("replace_order_res=" + json.dumps(res.json(), indent=4))
    sleep(5)

    res = trade_client.order_v2.cancel_order_v2(account_id=account_id, client_order_id=client_order_id)
    if res.status_code == 200:
        print("cancel_order_res=" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v2.get_order_history_request(account_id=account_id)
    if res.status_code == 200:
        print("order_history_res=" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v2.get_order_open(account_id=account_id)
    if res.status_code == 200:
        print("order_open_res=" + json.dumps(res.json(), indent=4))

    # order detail
    res = trade_client.order_v2.get_order_detail(account_id=account_id, client_order_id=client_order_id)
    if res.status_code == 200:
        print("order detail=" + json.dumps(res.json(), indent=4))

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
    res = trade_client.order_v2.preview_option(account_id, option_new_orders)
    if res.status_code == 200:
        print("preview option=" + json.dumps(res.json(), indent=4))
    sleep(5)
    # place

    # This is an optional feature; you can still make a request without setting it.
    custom_headers_map = {"category": Category.US_OPTION.name}
    trade_client.order_v2.add_custom_headers(custom_headers_map)
    res = trade_client.order_v2.place_option(account_id, option_new_orders)
    trade_client.order_v2.remove_custom_headers()
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
    res = trade_client.order_v2.replace_option(account_id, option_modify_orders)
    if res.status_code == 200:
        print("replace option=" + json.dumps(res.json(), indent=4))
    sleep(5)

    # cancel
    res = trade_client.order_v2.cancel_option(account_id, client_order_id)
    if res.status_code == 200:
        print("cancel option=" + json.dumps(res.json(), indent=4))