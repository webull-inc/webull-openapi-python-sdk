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
from webull.data.request.get_event_depth_request import GetEventDepthRequest
from webull.data.request.get_event_snapshot_request import GetEventSnapshotRequest

class EventMarketData:
    def __init__(self, api_client):
        self.client = api_client

    def get_event_snapshot(self, symbols, category=Category.US_EVENT.name):
        """
        Get real-time market snapshot data for a event instrument. Price unit is based on usd_cent.

        :param symbols: Symbol of the event market, supports JSON array format, multiple symbols separated by commas; maximum 100 symbols per query.
        :param category: default is US_EVENT, currently only US_EVENT is supported.
        """
        snapshot_request = GetEventSnapshotRequest()
        snapshot_request.set_symbols(symbols)
        snapshot_request.set_category(category)
        response = self.client.get_response(snapshot_request)
        return response

    def get_event_depth(self, symbol, category=Category.US_EVENT.name, depth=10):
        """
        Get the current order book for a specific event instrument.
        The order book shows all active bid orders for both yes and no sides of a binary market.
        It returns yes bids and no bids only (no asks are returned). Price unit is based on usd_cent.

        :param symbol:Symbol of the event market.
        :param category: default is US_EVENT, currently only US_EVENT is supported.
        :param depth: Depth of buying and selling orders, default 10 levels, etc.
        """
        quote_request = GetEventDepthRequest()
        quote_request.set_symbol(symbol)
        quote_request.set_category(category)
        quote_request.set_depth(depth)
        response = self.client.get_response(quote_request)
        return response