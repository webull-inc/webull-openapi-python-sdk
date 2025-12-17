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
        print("preview option res:", res.json())

    # place
    res = trade_client.order_v2.place_option(account_id, option_new_orders)
    if res.status_code == 200:
        print("place option res:" , res.json())

    option_modify_orders = [
        {
            "client_order_id": client_order_id,
            "quantity": "2",
            "limit_price": "21.25"
        }
    ]
    res = trade_client.order_v2.replace_option(account_id, option_modify_orders)
    if res.status_code == 200:
        print("Replace option order res:" , res.json())

    res = trade_client.order_v2.cancel_option(account_id, client_order_id)
    if res.status_code == 200:
        print("Cancel option order res:" , res.json())

    res = trade_client.order_v2.get_order_detail(account_id, client_order_id)
    if res.status_code == 200:
        print("Option order detail order res:" , res.json())