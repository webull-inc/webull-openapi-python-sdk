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

from webull.data.request.get_option_bars_request import GetOptionBarsRequest
from webull.data.request.get_option_snapshot_request import GetOptionSnapshotRequest
from webull.data.request.get_option_tick_request import GetOptionTickRequest


class OptionMarketData:
    def __init__(self, api_client):
        self.client = api_client

    def get_option_history_bars(self, symbols, category, timespan, count='200', real_time_required=None):
        """
        Batch query K-line data for multiple option symbols, returning aggregated data within the window.
        According to the last N K-lines of the option code, it supports various granularity K-lines such as m1 and m5.

        :param symbols: List of option security codes
        :param category: Security type, enumeration
        :param timespan: K-line interval
        :param count: Number of K-lines to return, default is 200, maximum is 1200
        :param real_time_required: Returns the latest trade quote data. By default, the most recent market data is returned.
        """
        history_bar_request = GetOptionBarsRequest()
        history_bar_request.set_symbols(symbols)
        history_bar_request.set_category(category)
        history_bar_request.set_timespan(timespan)
        history_bar_request.set_count(count)
        history_bar_request.set_real_time_required(real_time_required)
        response = self.client.get_response(history_bar_request)
        return response

    def get_option_tick(self, symbol, category, count='30'):
        """
        Query tick-by-tick transaction of options according to the option code list.

        :param symbol: Option securities code
        :param category: Security type, enumeration.
        :param count: The number of lines: the default is 30, and the maximum limit is 1200
        """
        tick_request = GetOptionTickRequest()
        tick_request.set_symbol(symbol)
        tick_request.set_category(category)
        tick_request.set_count(count)
        response = self.client.get_response(tick_request)
        return response

    def get_option_snapshot(self, symbols, category):
        """
        Query the latest option market snapshots in batches according to the option code list.

        :param symbols: List of option security codes; for example: single: AAPL260522C00300000 multiple: AAPL260522C00300000,TSLA251219C00450000;
        For each request,up to 20 symbols can be subscribed
        :param category: Security type, enumeration.
        """
        snapshot_request = GetOptionSnapshotRequest()
        snapshot_request.set_symbols(symbols)
        snapshot_request.set_category(category)
        response = self.client.get_response(snapshot_request)
        return response
