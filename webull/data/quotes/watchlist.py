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

from webull.data.request.watchlist.create_watchlist_request import CreateWatchlistRequest
from webull.data.request.watchlist.delete_watchlist_request import DeleteWatchlistRequest
from webull.data.request.watchlist.update_watchlist_request import UpdateWatchlistRequest
from webull.data.request.watchlist.get_watchlist_request import GetWatchlistRequest
from webull.data.request.watchlist.add_watchlist_instruments_request import AddWatchlistInstrumentsRequest
from webull.data.request.watchlist.remove_watchlist_instruments_request import RemoveWatchlistInstrumentsRequest
from webull.data.request.watchlist.update_watchlist_instruments_request import UpdateWatchlistInstrumentsRequest
from webull.data.request.watchlist.get_watchlist_instruments_request import GetWatchlistInstrumentsRequest


class Watchlist:
    def __init__(self, api_client):
        self.client = api_client

    def create_watchlist(self, name, sort=None):
        """
        Create a new watchlist.
        Maximum 20 watchlists can be created (shared with retail).

        :param name: Watchlist name. Maximum 20 watchlists can be created.
        :param sort: Sort order number (optional).
        :return: Response containing the new watchlist_id.
        """
        request = CreateWatchlistRequest()
        request.set_name(name)
        request.set_sort(sort)
        response = self.client.get_response(request)
        return response

    def delete_watchlist(self, watchlist_id):
        """
        Delete a watchlist and all instruments in it. This operation is irreversible.

        :param watchlist_id: Watchlist unique identifier.
        :return: Response containing success status.
        """
        request = DeleteWatchlistRequest()
        request.set_watchlist_id(watchlist_id)
        response = self.client.get_response(request)
        return response

    def update_watchlist(self, watchlist_id, name=None, sort=None):
        """
        Update an existing watchlist's properties such as name or sort order.
        Only provided fields will be updated; unprovided fields remain unchanged.

        :param watchlist_id: Watchlist unique identifier.
        :param name: New watchlist name (optional).
        :param sort: New sort order number (optional).
        :return: Response containing success status.
        """
        request = UpdateWatchlistRequest()
        request.set_watchlist_id(watchlist_id)
        request.set_name(name)
        request.set_sort(sort)
        response = self.client.get_response(request)
        return response

    def get_watchlist(self):
        """
        Get all watchlists for the current user, sorted by sort order in descending order.

        :return: List of watchlists containing watchlist_id, name, sort, create_time, update_time.
        """
        request = GetWatchlistRequest()
        response = self.client.get_response(request)
        return response

    def add_instruments(self, watchlist_id, instruments):
        """
        Add one or more instruments to an existing watchlist.
        Currently does not support EC contracts, futures, or options.
        Maximum 1000 instruments total across all watchlists.

        :param watchlist_id: Watchlist unique identifier.
        :param instruments: List of instruments to add. Each instrument should contain:
            - symbol: Instrument symbol (e.g., AAPL)
            - category: Instrument category (e.g., US_STOCK, US_CRYPTO)
            - sort: Sort order number
        :return: Response containing success status.
        """
        request = AddWatchlistInstrumentsRequest()
        request.set_watchlist_id(watchlist_id)
        request.set_instruments(instruments)
        response = self.client.get_response(request)
        return response

    def remove_instruments(self, watchlist_id, instruments):
        """
        Remove one or more instruments from a watchlist by symbol and category.

        :param watchlist_id: Watchlist unique identifier.
        :param instruments: List of instruments to remove. Each instrument should contain:
            - symbol: Instrument symbol (e.g., AAPL)
            - category: Instrument category (e.g., US_STOCK)
        :return: Response containing success status.
        """
        request = RemoveWatchlistInstrumentsRequest()
        request.set_watchlist_id(watchlist_id)
        request.set_instruments(instruments)
        response = self.client.get_response(request)
        return response

    def update_instruments(self, watchlist_id, instruments):
        """
        Update the sort order of instruments in a watchlist.

        :param watchlist_id: Watchlist unique identifier.
        :param instruments: List of instruments to update. Each instrument should contain:
            - symbol: Instrument symbol (for locating)
            - category: Instrument category (for locating)
            - sort: New sort order number
        :return: Response containing success status.
        """
        request = UpdateWatchlistInstrumentsRequest()
        request.set_watchlist_id(watchlist_id)
        request.set_instruments(instruments)
        response = self.client.get_response(request)
        return response

    def get_instruments(self, watchlist_id):
        """
        Get all instruments in a watchlist, sorted by sort_order in descending order.

        :param watchlist_id: Watchlist unique identifier.
        :return: Response containing watchlist_id and list of instruments with
            instrument_id, symbol, name, exchange_code, sort, added_time.
        """
        request = GetWatchlistInstrumentsRequest()
        request.set_watchlist_id(watchlist_id)
        response = self.client.get_response(request)
        return response
