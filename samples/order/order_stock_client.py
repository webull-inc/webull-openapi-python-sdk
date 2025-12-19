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

import uuid
from webull.core.client import ApiClient
from webull.trade.trade_client import TradeClient

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>" # hk or us
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


    # simple order
    client_order_id = uuid.uuid4().hex
    print('client order id:', client_order_id)
    new_simple_orders = [
        {
            "client_order_id": client_order_id,
            "symbol": "BULL",
            "instrument_type": "EQUITY",
            "market": "US",
            "order_type": "LIMIT",
            "limit_price": "26",
            "quantity": "1",
            "support_trading_session": "CORE",
            "side": "BUY",
            "time_in_force": "DAY",
            "entrust_type": "QTY"
        }
    ]
    new_hk_stock_simple_orders = [
        {
            "client_order_id": client_order_id,
            "symbol": "00700",
            "instrument_type": "EQUITY",
            "market": "HK",
            "order_type": "ENHANCED_LIMIT",
            "limit_price": "612",
            "quantity": "100",
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

    modify_simple_orders = [
        {
            "client_order_id": client_order_id,
            "quantity": "2",
            "limit_price": "25"
        }
    ]
    res = trade_client.order_v2.replace_order(account_id, modify_simple_orders)
    if res.status_code == 200:
        print('replace order res:', res.json())

    res = trade_client.order_v2.cancel_order(account_id, client_order_id)
    if res.status_code == 200:
        print('cancel order res:', res.json())

    res = trade_client.order_v2.get_order_detail(account_id, client_order_id)
    if res.status_code == 200:
        print('order detail:', res.json())
