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


class GetOptionSnapshotRequest(ApiRequest):
    """
    Request class for querying real-time quote snapshots for options.
    Returns key market indicators for specified options, including the latest price,
    price change percentage, trading volume, turnover rate, and best bid/ask quotes.
    """

    def __init__(self):
        ApiRequest.__init__(self, "/openapi/market-data/option/snapshot", version='v2', method="GET", query_params={})

    def set_symbols(self, symbols):
        """
        Set option symbols.
        
        :param symbols: List of option symbols, separated by commas; maximum 20 symbols per query.
                       Example: "AAPL260522C00300000,TSLA251219C00450000" or ["AAPL260522C00300000", "TSLA251219C00450000"]
        """
        if isinstance(symbols, str):
            self.add_query_param("symbols", symbols)
        elif isinstance(symbols, list):
            self.add_query_param("symbols", ",".join(symbols))

    def set_category(self, category):
        """
        Set security type.
        
        :param category: Security type. Currently only US_OPTION is supported.
        """
        self.add_query_param("category", category)
