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

from webull.data.common.category import Category
from webull.data.common.contract_type import ContractType
from webull.data.common.timespan import Timespan
from webull.core.client import ApiClient
from webull.data.data_client import DataClient

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"
# The token_dir parameter can be used to specify the directory for storing the 2FA token. Both absolute and relative paths are supported and this option has the highest priority.
# Alternatively, the storage directory can be configured via an environment variable with the key WEBULL_OPENAPI_TOKEN_DIR, which also supports both absolute and relative paths.
# If neither is specified, the default configuration will be used, and the token will be stored at conf/token.txt under the current working directory.
# token_dir = "<your_token_dir>"
# api_client.set_token_dir(token_dir)

api_client = ApiClient(your_app_key, your_app_secret, region_id)
api_client.add_endpoint(region_id, optional_api_endpoint)


if __name__ == '__main__':
    data_client = DataClient(api_client)

    trading_sessions = ["PRE", "RTH", "ATH", "OVN"]
    res = data_client.instrument.get_instrument("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_instrument:', res.json())

    res = data_client.instrument.get_crypto_instrument()
    if res.status_code == 200:
        print('get_crypto_instrument(all):', res.json())

    res = data_client.instrument.get_crypto_instrument("BTCUSD")
    if res.status_code == 200:
        print('get_crypto_instrument:', res.json())

    res = data_client.crypto_market_data.get_crypto_snapshot("BTCUSD")
    if res.status_code == 200:
        print('get_crypto_snapshot:', res.json())

    res = data_client.crypto_market_data.get_crypto_history_bar("BTCUSD", Category.US_CRYPTO.name, Timespan.M1.name)
    if res.status_code == 200:
        print('get_crypto_history_bar:', res.json())

    res = data_client.market_data.get_snapshot('AAPL', Category.US_STOCK.name, extend_hour_required=True, overnight_required=True)
    if res.status_code == 200:
        print('get_snapshot:', res.json())

    res = data_client.market_data.get_history_bar('AAPL', Category.US_STOCK.name, Timespan.M1.name)
    if res.status_code == 200:
        print('get_history_bar:', res.json())

    res = data_client.market_data.get_batch_history_bar(['AAPL', 'TSLA'], Category.US_STOCK.name, Timespan.M1.name, 1)
    if res.status_code == 200:
        print('get_batch_history_bar:', res.json())

    res = data_client.market_data.get_tick("AAPL", Category.US_STOCK.name, trading_sessions=trading_sessions)
    if res.status_code == 200:
        print('get_tick:', res.json())

    res = data_client.market_data.get_footprint("AAPL", Category.US_STOCK.name, Timespan.S5.name)
    if res.status_code == 200:
        print('get_footprint:', res.json())

    res = data_client.market_data.get_quotes("AAPL", Category.US_STOCK.name, depth=1, overnight_required=True)
    if res.status_code == 200:
        print('get_quotes:', res.json())

    res = data_client.futures_market_data.get_futures_depth("SILZ5", Category.US_FUTURES.name, depth=1)
    if res.status_code == 200:
        print('get_futures_depth:', res.json())

    res = data_client.futures_market_data.get_futures_history_bars('SILZ5,6BM6', Category.US_FUTURES.name, Timespan.M1.name)
    if res.status_code == 200:
        print('get_futures_history_bars:', res.json())

    res = data_client.futures_market_data.get_futures_tick("SILZ5", Category.US_FUTURES.name, count=10)
    if res.status_code == 200:
        print('get_futures_tick:', res.json())

    res = data_client.futures_market_data.get_futures_snapshot("SILZ5,6BM6", Category.US_FUTURES.name)
    if res.status_code == 200:
        print('get_futures_snapshot:', res.json())

    res = data_client.futures_market_data.get_futures_footprint("SILZ5,6BM6", Category.US_FUTURES.name, Timespan.S5.name)
    if res.status_code == 200:
        print('get_futures_footprint:', res.json())

    res = data_client.instrument.get_futures_products(Category.US_FUTURES.name)
    if res.status_code == 200:
        print('get_futures_products:', res.json())

    res = data_client.instrument.get_futures_instrument("ESZ5", Category.US_FUTURES.name)
    if res.status_code == 200:
        print('get_futures_instrument:', res.json())

    res = data_client.instrument.get_futures_instrument_by_code("ES", Category.US_FUTURES.name, ContractType.MONTHLY.name)
    if res.status_code == 200:
        print('get_futures_instrument_by_code:', res.json())