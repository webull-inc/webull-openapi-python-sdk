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
from webull.data.request.get_futures_footprint_request import GetFuturesFootprintRequest
from webull.data.request.get_futures_historical_bars_request import GetFuturesHistoricalBarsRequest
from webull.data.request.get_futures_snapshot_request import GetFuturesSnapshotRequest
from webull.data.request.get_futures_depth_request import GetFuturesDepthRequest
from webull.data.request.get_futures_tick_request import GetFuturesTickRequest

class FuturesMarketData:
    def __init__(self, api_client):
        self.client = api_client

    def get_futures_history_bars(self, symbols, category, timespan, count='200', real_time_required=None):
        """
        Batch query K-line data for multiple futures symbols, returning aggregated data within the window.
        According to the last N K-lines of the futures code, it supports various granularity K-lines such as m1 and m5.

        :param symbols: List of futures security codes
        :param category: Security type, enumeration
        :param timespan: K-line interval
        :param count: Number of K-lines to return, default is 200, maximum is 1200
        :param real_time_required: Returns the latest trade quote data. By default, the most recent market data is returned.
        """
        history_bar_request = GetFuturesHistoricalBarsRequest()
        history_bar_request.set_symbols(symbols)
        history_bar_request.set_category(category)
        history_bar_request.set_timespan(timespan)
        history_bar_request.set_count(count)
        history_bar_request.set_real_time_required(real_time_required)
        response = self.client.get_response(history_bar_request)
        return response

    def get_futures_snapshot(self, symbols, category):
        """
        Query the latest futures market snapshots in batches according to the futures code list.

        :param symbols: List of futures security codes; for example: single: ESZ3 multiple: ESZ3,NQZ3;
        For each request,up to 100 symbols can be subscribed
        :param category: Security type, enumeration.
        """
        snapshot_request = GetFuturesSnapshotRequest()
        snapshot_request.set_symbols(symbols)
        snapshot_request.set_category(category)
        response = self.client.get_response(snapshot_request)
        return response

    def get_futures_depth(self, symbol, category, depth=None):
        """
        Query the depth quote of futures according to the futures code list.

        :param symbol: Futures securities code
        :param category: Security type, enumeration.
        :param depth: Retrieve bid/ask depth
        Level 1 contains only the top 1 bid/ask level.
        Level 2 becomes effective, with 10 levels by default. For U.S. futures, Level 2 supports up to 50 levels.
        """
        quote_request = GetFuturesDepthRequest()
        quote_request.set_symbol(symbol)
        quote_request.set_category(category)
        quote_request.set_depth(depth)
        response = self.client.get_response(quote_request)
        return response

    def get_futures_tick(self, symbol, category, count='200'):
        """
        Query tick-by-tick transaction of futures according to the futures code list.

        :param symbol: Futures securities code
        :param category: Security type, enumeration.
        :param count: The number of lines: the default is 30, and the maximum limit is 1200
        """
        tick_request = GetFuturesTickRequest()
        tick_request.set_symbol(symbol)
        tick_request.set_category(category)
        tick_request.set_count(count)
        response = self.client.get_response(tick_request)
        return response

    def get_futures_footprint(self, symbols, category, timespan, count=None,
                      real_time_required=None, trading_sessions=None):
        """
         Search the futures footprint based on the list of futures codes and futures types.

        :param symbols: Futures Securities symbol, such as: BITH6,BITF26.
        :param category: Security type, enumeration.
        :param timespan: Time granularity.
        :param count: Number of entries: 200 by default, maximum 1200.
        :param real_time_required: Whether to include the latest data or candlestick charts that are not yet finalized. The default is false, meaning they are not included. This option is only used for minute candlestick charts.
        :param trading_sessions: RTH: During trading hours, PRE: Before trading hours, ATH: After trading hours. Default: RTH.
        """
        footprint_request = GetFuturesFootprintRequest()
        footprint_request.set_symbols(symbols)
        footprint_request.set_category(category)
        footprint_request.set_timespan(timespan)
        footprint_request.set_count(count)
        footprint_request.set_real_time_required(real_time_required)
        footprint_request.set_trading_sessions(trading_sessions)
        response = self.client.get_response(footprint_request)
        return response