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

    # Get top gainers for today (stocks with highest price increase)
    res = data_client.screener.get_gainers_losers(
        rank_type="DAY_1",
        category="US_STOCK",
        sort_by="CHANGE_RATIO",
        direction="DESC",
        page_size=10
    )
    if res.status_code == 200:
        print('get_gainers (day):', res.json())

    # Get top losers for today (stocks with highest price decrease)
    res = data_client.screener.get_gainers_losers(
        rank_type="DAY_1",
        category="US_STOCK",
        sort_by="CHANGE_RATIO",
        direction="ASC",
        page_size=10
    )
    if res.status_code == 200:
        print('get_losers (day):', res.json())

    # Get pre-market movers
    res = data_client.screener.get_gainers_losers(
        rank_type="PRE_MARKET",
        category="US_STOCK",
        sort_by="CHANGE_RATIO",
        direction="DESC",
        page_size=20
    )
    if res.status_code == 200:
        print('get_pre_market_movers:', res.json())

    # Get 52-week top performers
    res = data_client.screener.get_gainers_losers(
        rank_type="WEEK_52",
        category="US_STOCK",
        sort_by="CHANGE_RATIO",
        direction="DESC",
        page_size=10
    )
    if res.status_code == 200:
        print('get_52_week_top_performers:', res.json())

    # Get most active stocks by volume
    res = data_client.screener.get_most_active(
        category="US_STOCK",
        rank_type="VOLUME",
        sort_by="VOLUME",
        direction="DESC",
        page_size=10
    )
    if res.status_code == 200:
        print('get_most_active_by_volume:', res.json())

    # Get stocks with unusual trading activity (high relative volume)
    res = data_client.screener.get_most_active(
        category="US_STOCK",
        rank_type="RELATIVE_VOLUME_10D",
        sort_by="RELATIVE_VOLUME_10D",
        direction="DESC",
        page_size=10
    )
    if res.status_code == 200:
        print('get_unusual_volume_activity:', res.json())

    # Get most active stocks by turnover amount
    res = data_client.screener.get_most_active(
        category="US_STOCK",
        rank_type="TURNOVER",
        sort_by="TURNOVER",
        direction="DESC",
        page_size=10
    )
    if res.status_code == 200:
        print('get_most_active_by_turnover:', res.json())

    # Get stocks with high price amplitude
    res = data_client.screener.get_most_active(
        category="US_STOCK",
        rank_type="AMPLITUDE",
        sort_by="AMPLITUDE",
        direction="DESC",
        page_size=10
    )
    if res.status_code == 200:
        print('get_high_amplitude_stocks:', res.json())
