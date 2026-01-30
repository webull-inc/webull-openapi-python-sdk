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

    # ============================================================
    # Equity Order Example
    # ============================================================

    # normal equity order
    normal_equity_client_order_id = uuid.uuid4().hex
    print('client order id:', normal_equity_client_order_id)
    new_normal_equity_orders = [
        {
            "combo_type": "NORMAL",
            "client_order_id": normal_equity_client_order_id,
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

    res = trade_client.order_v3.preview_order(account_id, new_normal_equity_orders)
    if res.status_code == 200:
        print('preview normal equity order res:', res.json())

    res = trade_client.order_v3.place_order(account_id, new_normal_equity_orders)
    if res.status_code == 200:
        print('place normal equity order res:', res.json())
    sleep(3)

    replace_normal_equity_orders = [
        {
            "client_order_id": normal_equity_client_order_id,
            "quantity": "100",
            "limit_price": "200"
        }
    ]
    res = trade_client.order_v3.replace_order(account_id, replace_normal_equity_orders)
    if res.status_code == 200:
        print('replace normal equity order res:', res.json())
    sleep(3)

    res = trade_client.order_v3.cancel_order(account_id, normal_equity_client_order_id)
    if res.status_code == 200:
        print('cancel normal equity order res:', res.json())

    res = trade_client.order_v3.get_order_open(account_id=account_id)
    if res.status_code == 200:
        print("order_open_res=" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v3.get_order_history(account_id)
    if res.status_code == 200:
        print('get order history res:', res.json())

    res = trade_client.order_v3.get_order_detail(account_id, normal_equity_client_order_id)
    if res.status_code == 200:
        print('get order detail res:', res.json())



    # combo equity order
    master_equity_client_order_id = uuid.uuid4().hex
    stop_profit_equity_client_order_id = uuid.uuid4().hex
    stop_loss_equity_client_order_id = uuid.uuid4().hex
    print('normal_equity_master_client_order_id:', master_equity_client_order_id)
    print('stop_profit_equity_client_order_id:', stop_profit_equity_client_order_id)
    print('stop_loss_equity_client_order_id:', stop_loss_equity_client_order_id)
    new_combo_orders = [
        {
            "client_order_id": master_equity_client_order_id,
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
            "client_order_id": stop_profit_equity_client_order_id,
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
            "client_order_id": stop_loss_equity_client_order_id,
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

    res = trade_client.order_v3.preview_order(account_id, new_combo_orders)
    if res.status_code == 200:
        print('preview combo equity order res:', res.json())

    res = trade_client.order_v3.place_order(account_id, new_combo_orders)
    if res.status_code == 200:
        print('place combo equity order res:', res.json())
    sleep(3)

    replace_combo_orders = [
        {
            "client_order_id": master_equity_client_order_id,
            "quantity": "2"
        },
        {
            "client_order_id": stop_profit_equity_client_order_id,
            "quantity": "2"
        },
        {
            "client_order_id": stop_loss_equity_client_order_id,
            "quantity": "2"
        }
    ]
    res = trade_client.order_v3.replace_order(account_id, replace_combo_orders)
    if res.status_code == 200:
        print('replace combo equity order res:', res.json())
    sleep(3)

    res = trade_client.order_v3.cancel_order(account_id, master_equity_client_order_id)
    if res.status_code == 200:
        print('cancel master equity order res:', res.json())

    res = trade_client.order_v3.get_order_history(account_id)
    if res.status_code == 200:
        print('get order history res:', res.json())

    res = trade_client.order_v3.get_order_open(account_id=account_id)
    if res.status_code == 200:
        print("order_open_res=" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v3.get_order_detail(account_id, master_equity_client_order_id)
    if res.status_code == 200:
        print('get master order detail res:', res.json())

    # batch place order
    batch_place_orders = [
        {
            "combo_type": "NORMAL",
            "client_order_id": uuid.uuid4().hex,
            "instrument_type": "EQUITY",
            "market": "US",
            "symbol": "AAPL",
            "order_type": "MARKET",
            "entrust_type": "QTY",
            "support_trading_session": "CORE",
            "time_in_force": "DAY",
            "side": "BUY",
            "quantity": "1"
        },
        {
            "combo_type": "NORMAL",
            "client_order_id": uuid.uuid4().hex,
            "instrument_type": "EQUITY",
            "market": "US",
            "symbol": "TESL",
            "order_type": "MARKET",
            "entrust_type": "QTY",
            "support_trading_session": "CORE",
            "time_in_force": "DAY",
            "side": "BUY",
            "quantity": "1"
        }
    ]
    res = trade_client.order_v3.batch_place_order(account_id, batch_place_orders)
    if res.status_code == 200:
        print('batch place normal equity order res:', res.json())


    # ============================================================
    # Option Order Example
    # ============================================================

    # normal option order
    normal_option_client_order_id = uuid.uuid4().hex
    new_normal_option_orders = [
        {
            "client_order_id": normal_option_client_order_id,
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
    res = trade_client.order_v3.preview_order(account_id, new_normal_option_orders)
    if res.status_code == 200:
        print("preview normal option order res:" + json.dumps(res.json(), indent=4))

    # place
    res = trade_client.order_v3.place_order(account_id, new_normal_option_orders)
    if res.status_code == 200:
        print("place normal option order res:" + json.dumps(res.json(), indent=4))
    sleep(3)

    # replace for Webull HK
    # replace_normal_option_orders = [
    #     {
    #         "client_order_id": normal_option_client_order_id,
    #         "quantity": "2",
    #         "limit_price": "11.3"
    #     }
    # ]
    # res = trade_client.order_v3.replace_option(account_id, replace_normal_option_orders)
    # if res.status_code == 200:
    #     print("replace normal option order res:" + json.dumps(res.json(), indent=4))
    # sleep(5)

    # replace for Webull US
    res = trade_client.order_v3.get_order_detail(account_id, normal_option_client_order_id)
    if res.status_code == 200:
        print('get normal option order detail res:', res.json())
    data = res.json() or {}
    leg_id = (
        data.get("orders", [{}])[0]
        .get("legs", [{}])[0]
        .get("id")
    )
    print('get normal option order detail id :', leg_id)

    # If it is a multi-leg option, you need to manually match it to the corresponding sub-leg orderId.
    if leg_id:
        replace_normal_option_orders = [
            {
                "client_order_id": normal_option_client_order_id,
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
        res = trade_client.order_v3.replace_order(account_id, replace_normal_option_orders)
        if res.status_code == 200:
            print("replace normal option order res:" + json.dumps(res.json(), indent=4))
        sleep(3)

    # cancel
    res = trade_client.order_v3.cancel_order(account_id, normal_option_client_order_id)
    if res.status_code == 200:
        print("cancel normal option order res:" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v3.get_order_history(account_id)
    if res.status_code == 200:
        print('get order history res:', res.json())

    res = trade_client.order_v3.get_order_open(account_id=account_id)
    if res.status_code == 200:
        print("order_open_res=" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v3.get_order_detail(account_id, normal_option_client_order_id)
    if res.status_code == 200:
        print('get option order detail res:', res.json())



    # ============================================================
    # Crypto Order Example
    # For the cryptocurrency example, please use a cryptocurrency account ID.
    # ============================================================

    # normal crypto order
    normal_crypto_client_order_id = uuid.uuid4().hex
    print('client order id:', normal_crypto_client_order_id)
    new_normal_crypto_orders = [
        {
            "combo_type": "NORMAL",
            "client_order_id": normal_crypto_client_order_id,
            "symbol": "BTCUSD",
            "instrument_type": "CRYPTO",
            "market": "US",
            "order_type": "LIMIT",
            "limit_price": "80000",
            "quantity": "0.003",
            "side": "BUY",
            "time_in_force": "DAY",
            "entrust_type": "QTY"
        }
    ]

    res = trade_client.order_v3.place_order(account_id, new_normal_crypto_orders)
    if res.status_code == 200:
        print('place normal crypto order res:', res.json())
    sleep(3)

    res = trade_client.order_v3.cancel_order(account_id, normal_crypto_client_order_id)
    if res.status_code == 200:
        print('cancel normal crypto order res:', res.json())

    res = trade_client.order_v3.get_order_open(account_id=account_id)
    if res.status_code == 200:
        print("order_open_res=" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v3.get_order_history(account_id)
    if res.status_code == 200:
        print('get order history res:', res.json())

    res = trade_client.order_v3.get_order_detail(account_id, normal_crypto_client_order_id)
    if res.status_code == 200:
        print('get order detail res:', res.json())



    # ============================================================
    # Futures Order Example
    # ============================================================

    # normal futures order
    normal_futures_client_order_id = uuid.uuid4().hex
    print('futures client order id:', normal_futures_client_order_id)
    new_normal_futures_orders = [
        {
            "combo_type": "NORMAL",
            "client_order_id": normal_futures_client_order_id,
            "symbol": "ESZ5",
            "instrument_type": "FUTURES",
            "market": "US",
            "order_type": "LIMIT",
            "limit_price": "4500",
            "quantity": "1",
            "side": "BUY",
            "time_in_force": "DAY",
            "entrust_type": "QTY"
        }
    ]
    res = trade_client.order_v3.place_order(account_id, new_normal_futures_orders)
    if res.status_code == 200:
        print('place normal futures order res:', res.json())
    sleep(3)

    # normal futures order replace
    replace_normal_futures_orders = [
        {
            "client_order_id": normal_futures_client_order_id,
            "quantity": "2",
            "limit_price": "4550"
        }
    ]
    res = trade_client.order_v3.replace_order(account_id, replace_normal_futures_orders)
    if res.status_code == 200:
        print('replace normal futures order res:', res.json())
    sleep(3)

    # normal futures order cancel
    res = trade_client.order_v3.cancel_order(account_id, normal_futures_client_order_id)
    if res.status_code == 200:
        print('cancel normal futures order res:', res.json())

    # get futures order detail
    res = trade_client.order_v3.get_order_detail(account_id, normal_futures_client_order_id)
    if res.status_code == 200:
        print('get futures order detail res:', res.json())

    # get futures open orders
    res = trade_client.order_v3.get_order_open(account_id, page_size=10)
    if res.status_code == 200:
        print("order_open_res=" + json.dumps(res.json(), indent=4))

    # get futures order history
    res = trade_client.order_v3.get_order_history(account_id, page_size=10)
    if res.status_code == 200:
        print('get order history res:', res.json())

    # ============================================================
    # Algo Order Example
    # ============================================================
    alog_client_order_id = uuid.uuid4().hex
    print('client order id:', alog_client_order_id)
    new_normal_equity_orders = [
        {
            "combo_type": "NORMAL",
            "client_order_id": alog_client_order_id,
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
            "algo_start_time": "16:00:00",
            "algo_end_time": "23:00:00",
            "target_vol_percent": "10",
            "algo_type": "POV"
        }
    ]

    res = trade_client.order_v3.preview_order(account_id, new_normal_equity_orders)
    if res.status_code == 200:
        print('preview algo order res:', res.json())

    res = trade_client.order_v3.place_order(account_id, new_normal_equity_orders)
    if res.status_code == 200:
        print('place algo order res:', res.json())
    sleep(3)

    replace_normal_equity_orders = [
        {
            "client_order_id": alog_client_order_id,
            "quantity": "100",
            "limit_price": "200"
        }
    ]
    res = trade_client.order_v3.replace_order(account_id, replace_normal_equity_orders)
    if res.status_code == 200:
        print('replace algo order res:', res.json())
    sleep(3)

    res = trade_client.order_v3.cancel_order(account_id, alog_client_order_id)
    if res.status_code == 200:
        print('cancel algo order res:', res.json())

    res = trade_client.order_v3.get_order_open(account_id=account_id)
    if res.status_code == 200:
        print("order_open_res=" + json.dumps(res.json(), indent=4))

    res = trade_client.order_v3.get_order_history(account_id)
    if res.status_code == 200:
        print('get order history res:', res.json())

    res = trade_client.order_v3.get_order_detail(account_id, alog_client_order_id)
    if res.status_code == 200:
        print('get order detail res:', res.json())
