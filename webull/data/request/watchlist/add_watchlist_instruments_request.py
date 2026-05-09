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

from webull.core.request import ApiRequest


class AddWatchlistInstrumentsRequest(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/openapi/market-data/watchlist/instruments/add", version="v2", method="POST", body_params={})

    def set_watchlist_id(self, watchlist_id):
        """
        Set the watchlist unique identifier.

        :param watchlist_id: Watchlist unique identifier.
        """
        self.add_body_params("watchlist_id", watchlist_id)

    def set_instruments(self, instruments):
        """
        Set the list of instruments to add.

        :param instruments: List of instruments to add. Each instrument should contain:
            - symbol: Instrument symbol (e.g., AAPL)
            - category: Instrument category (e.g., US_STOCK, US_CRYPTO)
            - sort: Sort order number
        """
        self.add_body_params("instruments", instruments)
