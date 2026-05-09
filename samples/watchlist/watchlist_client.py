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

    # Get all watchlists
    res = data_client.watchlist.get_watchlist()
    if res.status_code == 200:
        print('get_watchlist:', res.json())

    # Create a new watchlist (max 20 watchlists, shared with retail)
    res = data_client.watchlist.create_watchlist(name="Tech Stocks", sort=1)
    if res.status_code == 200:
        print('create_watchlist:', res.json())
        watchlist_id = res.json().get("watchlist_id")

        # Update the watchlist
        res = data_client.watchlist.update_watchlist(
            watchlist_id=watchlist_id,
            name="My Favorites",
            sort=2
        )
        if res.status_code == 200:
            print('update_watchlist:', res.json())

        # Add instruments to the watchlist (max 1000 instruments total)
        instruments = [
            {"symbol": "AAPL", "category": "US_STOCK", "sort": 1},
            {"symbol": "TSLA", "category": "US_STOCK", "sort": 2}
        ]
        res = data_client.watchlist.add_instruments(watchlist_id, instruments)
        if res.status_code == 200:
            print('add_instruments:', res.json())

        # Get instruments in the watchlist
        res = data_client.watchlist.get_instruments(watchlist_id)
        if res.status_code == 200:
            print('get_instruments:', res.json())

        # Update instruments sort order
        instruments = [
            {"symbol": "AAPL", "category": "US_STOCK", "sort": 3},
            {"symbol": "TSLA", "category": "US_STOCK", "sort": 1}
        ]
        res = data_client.watchlist.update_instruments(watchlist_id, instruments)
        if res.status_code == 200:
            print('update_instruments:', res.json())

        # Remove instruments from the watchlist
        instruments = [
            {"symbol": "AAPL", "category": "US_STOCK"},
            {"symbol": "TSLA", "category": "US_STOCK"}
        ]
        res = data_client.watchlist.remove_instruments(watchlist_id, instruments)
        if res.status_code == 200:
            print('remove_instruments:', res.json())

        # Delete the watchlist (irreversible)
        res = data_client.watchlist.delete_watchlist(watchlist_id)
        if res.status_code == 200:
            print('delete_watchlist:', res.json())
