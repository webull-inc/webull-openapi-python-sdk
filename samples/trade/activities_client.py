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

    # Query cash activities with default parameters
    res = trade_client.activity.get_activities(account_id)
    if res.status_code == 200:
        print('get activities:', res.json())

    # Query cash activities with activity type filter
    res = trade_client.activity.get_activities(account_id, activity_types="TRADE,DEPOSIT")
    if res.status_code == 200:
        print('get activities by type:', res.json())

    # Query cash activities with time range filter
    res = trade_client.activity.get_activities(
        account_id,
        start_time="2026-06-30T12:00:00.000Z",
        end_time="2026-07-03T12:00:00.000Z",
        page_size=20
    )
    if res.status_code == 200:
        print('get activities by time range:', res.json())

    # Query cash activities with cursor-based pagination
    res = trade_client.activity.get_activities(
        account_id,
        last_activity_id="<last_activity_id_from_previous_page>",
        page_size=10
    )
    if res.status_code == 200:
        print('get activities next page:', res.json())
