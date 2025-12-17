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

    res = trade_client.account_v2.get_account_list()
    if res.status_code == 200:
        print('get account list:', res.json())

    res = trade_client.account_v2.get_account_balance(account_id)
    if res.status_code == 200:
        print('get account balance res:', res.json())

    res = trade_client.account_v2.get_account_position(account_id)
    if res.status_code == 200:
        print('get account position res:', res.json())

    # simple order
    client_order_id = uuid.uuid4().hex
    print('client order id:', client_order_id)
    new_simple_orders = [
        {
            "combo_type": "NORMAL",
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
            "entrust_type": "QTY"
        }
    ]

    res = trade_client.order_v2.preview_order(account_id, new_simple_orders)
    if res.status_code == 200:
        print('preview order res:', res.json())

    res = trade_client.order_v2.place_order(account_id, new_simple_orders)
    if res.status_code == 200:
        print('place order res:', res.json())
    sleep(3)

    modify_simple_orders = [
        {
            "client_order_id": client_order_id,
            "quantity": "100",
            "limit_price": "200"
        }
    ]
    res = trade_client.order_v2.replace_order(account_id, modify_simple_orders)
    if res.status_code == 200:
        print('replace order res:', res.json())
    sleep(3)

    res = trade_client.order_v2.cancel_order(account_id, client_order_id)
    if res.status_code == 200:
        print('cancel order res:', res.json())

    res = trade_client.order_v2.get_order_open(account_id=account_id)
    if res.status_code == 200:
        print("order_open_res=" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v2.get_order_history(account_id)
    if res.status_code == 200:
        print('get order history res:', res.json())

    res = trade_client.order_v2.get_order_detail(account_id, client_order_id)
    if res.status_code == 200:
        print('get order detail res:', res.json())



    # Combo Order
    master_client_order_id = uuid.uuid4().hex
    stop_profit_client_order_id = uuid.uuid4().hex
    stop_loss_client_order_id = uuid.uuid4().hex
    print('master_client_order_id:', master_client_order_id)
    print('stop_profit_client_order_id:', stop_profit_client_order_id)
    print('stop_loss_client_order_id:', stop_loss_client_order_id)
    new_combo_orders = [
        {
            "client_order_id": master_client_order_id,
            "combo_type": "MASTER",
            "symbol": "F",
            "instrument_type": "EQUITY",
            "market": "US",
            "order_type": "LIMIT",
            "quantity": "1",
            "support_trading_session": "N",
            "limit_price": "10.5",
            "side": "BUY",
            "entrust_type": "QTY",
            "time_in_force": "DAY"
        },
        {
            "client_order_id": stop_profit_client_order_id,
            "combo_type": "STOP_PROFIT",
            "symbol": "F",
            "instrument_type": "EQUITY",
            "market": "US",
            "order_type": "LIMIT",
            "quantity": "1",
            "support_trading_session": "N",
            "limit_price": "11.5",
            "side": "SELL",
            "entrust_type": "QTY",
            "time_in_force": "DAY"
        },
        {
            "client_order_id": stop_loss_client_order_id,
            "combo_type": "STOP_LOSS",
            "symbol": "F",
            "instrument_type": "EQUITY",
            "market": "US",
            "order_type": "STOP_LOSS",
            "quantity": "1",
            "support_trading_session": "N",
            "stop_price": "10",
            "side": "SELL",
            "entrust_type": "QTY",
            "time_in_force": "DAY"
        }
    ]

    res = trade_client.order_v2.preview_order(account_id, new_combo_orders)
    if res.status_code == 200:
        print('preview combo order res:', res.json())

    res = trade_client.order_v2.place_order(account_id, new_combo_orders)
    if res.status_code == 200:
        print('place combo order res:', res.json())
    sleep(3)

    modify_combo_orders = [
        {
            "client_order_id": master_client_order_id,
            "quantity": "2"
        },
        {
            "client_order_id": stop_profit_client_order_id,
            "quantity": "2"
        },
        {
            "client_order_id": stop_loss_client_order_id,
            "quantity": "2"
        }
    ]
    res = trade_client.order_v2.replace_order(account_id, modify_combo_orders)
    if res.status_code == 200:
        print('replace combo order res:', res.json())
    sleep(3)

    res = trade_client.order_v2.cancel_order(account_id, master_client_order_id)
    if res.status_code == 200:
        print('cancel master order res:', res.json())

    res = trade_client.order_v2.get_order_history(account_id)
    if res.status_code == 200:
        print('get order history res:', res.json())

    res = trade_client.order_v2.get_order_open(account_id=account_id)
    if res.status_code == 200:
        print("order_open_res=" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v2.get_order_detail(account_id, master_client_order_id)
    if res.status_code == 200:
        print('get master order detail res:', res.json())


    # Options
    # For option order inquiries, please use the V2 query interface: api.order_v2.get_order_detail(account_id, client_order_id).
    client_order_id = uuid.uuid4().hex
    option_new_orders = [
        {
            "client_order_id": client_order_id,
            "combo_type": "NORMAL",
            "order_type": "LIMIT",
            "quantity": "1",
            "limit_price": "21.25",
            "option_strategy": "SINGLE",
            "side": "BUY",
            "time_in_force": "GTC",
            "entrust_type": "QTY",
            "legs": [
                {
                    "side": "BUY",
                    "quantity": "1",
                    "symbol": "TSLA",
                    "strike_price": "400",
                    "option_expire_date": "2025-12-26",
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
        print("preview option res:" + json.dumps(res.json(), indent=4))

    # place
    res = trade_client.order_v2.place_option(account_id, option_new_orders)
    if res.status_code == 200:
        print("place option res:" + json.dumps(res.json(), indent=4))
    sleep(3)

    # replace for Webull HK
    # option_modify_orders = [
    #     {
    #         "client_order_id": client_order_id,
    #         "quantity": "2",
    #         "limit_price": "11.3"
    #     }
    # ]
    # res = trade_client.order_v2.replace_option(account_id, option_modify_orders)
    # if res.status_code == 200:
    #     print("replace option res:" + json.dumps(res.json(), indent=4))
    # sleep(5)

    # replace for Webull US
    res = trade_client.order_v2.get_order_detail(account_id, client_order_id)
    if res.status_code == 200:
        print('get option order detail res:', res.json())
    data = res.json() or {}
    leg_id = (
        data.get("orders", [{}])[0]
        .get("legs", [{}])[0]
        .get("id")
    )
    print('get option order detail id :', leg_id)

    # If it is a multi-leg option, you need to manually match it to the corresponding sub-leg orderId.
    if leg_id:
        option_modify_orders = [
            {
                "client_order_id": client_order_id,
                "quantity": "2",
                "limit_price": "21.3",
                "legs": [
                    {
                        "id": leg_id,
                        "quantity": "2"
                    }
                ]
            }
        ]
        res = trade_client.order_v2.replace_option(account_id, option_modify_orders)
        if res.status_code == 200:
            print("replace option res:" + json.dumps(res.json(), indent=4))
        sleep(3)

    # cancel
    res = trade_client.order_v2.cancel_option(account_id, client_order_id)
    if res.status_code == 200:
        print("cancel option res:" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v2.get_order_history(account_id)
    if res.status_code == 200:
        print('get order history res:', res.json())

    res = trade_client.order_v2.get_order_open(account_id=account_id)
    if res.status_code == 200:
        print("order_open_res=" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v2.get_order_detail(account_id, client_order_id)
    if res.status_code == 200:
        print('get option order detail res:', res.json())