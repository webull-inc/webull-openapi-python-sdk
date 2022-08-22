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
from webull.data.common.timespan import Timespan
from webull.core.client import ApiClient
from webull.data.data_client import DataClient

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"
api_client = ApiClient(your_app_key, your_app_secret, region_id)
api_client.add_endpoint(region_id, optional_api_endpoint)

if __name__ == '__main__':
    data_client = DataClient(api_client)

    trading_sessions = ["PRE", "RTH", "ATH", "OVN"]
    res = data_client.instrument.get_instrument("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_instrument:', res.json())

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

    res = data_client.market_data.get_quotes("AAPL", Category.US_STOCK.name, depth=1, overnight_required=True)
    if res.status_code == 200:
        print('get_quotes:', res.json())


