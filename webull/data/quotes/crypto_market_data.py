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
from webull.data.common.category import Category
from webull.data.request.get_crypto_historical_bars_request import GetCryptoHistoricalBarsRequest
from webull.data.request.get_crypto_snapshot_request import GetCryptoSnapshotRequest


class CryptoMarketData:
    def __init__(self, api_client):
        self.client = api_client

    def get_crypto_history_bar(self, symbols, category, timespan, count='200', real_time_required=None):
        """
        Returns to Instrument in the window aggregated data.
        According to the last N K-lines of the stock code, it supports various granularity K-lines such as m1 and m5.
        Currently, only the K-line with the previous weight is provided for the daily K-line and above,
        and only the un-weighted K-line is provided for the minute K.

        :param symbols: List of security codes (e.g., single: 00700; multiple: BTCUSD,ETHUSD or ['BTCUSD','ETHUSD']).
        :param category: Security type. Fixed value: "US_CRYPTO"
        :param timespan: K-line time granularity
        :param count: The number of lines: the default is 200, and the maximum limit is 1200
        :param real_time_required: Returns the latest trade quote data. By default, the most recent market data is returned.
        By default, only intraday candlestick data is returned.
        """
        crypto_history_bar_request = GetCryptoHistoricalBarsRequest()
        crypto_history_bar_request.set_symbols(symbols)
        crypto_history_bar_request.set_category(category)
        crypto_history_bar_request.set_timespan(timespan)
        crypto_history_bar_request.set_count(count)
        crypto_history_bar_request.set_real_time_required(real_time_required)
        response = self.client.get_response(crypto_history_bar_request)
        return response

    def get_crypto_snapshot(self, symbols, category=Category.US_CRYPTO.name):
        """
        Query the latest crypto market snapshots in batches according to the security code list.

        :param symbols: List of security codes (e.g., single: 00700; multiple: BTCUSD,ETHUSD or ['BTCUSD','ETHUSD']).
        Up to 20 symbols can be subscribed per request.
        :param category: Security type. Fixed value: "US_CRYPTO".
        """
        crypto_snapshot_request = GetCryptoSnapshotRequest()
        crypto_snapshot_request.set_symbols(symbols)
        crypto_snapshot_request.set_category(category)
        response = self.client.get_response(crypto_snapshot_request)
        return response
