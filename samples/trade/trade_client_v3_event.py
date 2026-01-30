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

    # normal event order
    normal_event_client_order_id = uuid.uuid4().hex
    print('event client order id:', normal_event_client_order_id)
    new_normal_event_orders = [
        {
            "combo_type": "NORMAL",
            "client_order_id": normal_event_client_order_id,
            "instrument_type": "EVENT",
            "market": "US",
            "symbol": "KXRATECUTCOUNT-25DEC31-T9",
            "order_type": "LIMIT",
            "entrust_type": "QTY",
            "time_in_force": "DAY",
            "side": "BUY",
            "quantity": "1",
            "limit_price": "0.1",
            "event_outcome": "yes"
        }
    ]

    res = trade_client.order_v3.preview_order(account_id, new_normal_event_orders)
    if res.status_code == 200:
        print('preview normal event order res:', res.json())

    res = trade_client.order_v3.place_order(account_id, new_normal_event_orders)
    if res.status_code == 200:
        print('place normal event order res:', res.json())
    sleep(3)

    # normal event order replace
    replace_normal_event_orders = [
        {
            "client_order_id": normal_event_client_order_id,
            "quantity": "10",
            "limit_price": "0.1"
        }
    ]
    res = trade_client.order_v3.replace_order(account_id, replace_normal_event_orders)
    if res.status_code == 200:
        print('replace normal event order res:', res.json())
    sleep(3)

    # normal event order cancel
    res = trade_client.order_v3.cancel_order(account_id, normal_event_client_order_id)
    if res.status_code == 200:
        print('cancel normal event order res:', res.json())

    # get event order detail
    res = trade_client.order_v3.get_order_detail(account_id, normal_event_client_order_id)
    if res.status_code == 200:
        print('get event order detail res:', res.json())