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


class GetOptionBarsRequest(ApiRequest):
    """
    Request class for querying historical bars for options.
    Batch query interface to retrieve the last N bars based on option codes, 
    time granularity, and type. Supports various granularities like M1, M5, etc.
    """

    def __init__(self):
        ApiRequest.__init__(self, "/openapi/market-data/option/bars", version='v2', method="GET", query_params={})

    def set_symbols(self, symbols):
        """
        Set option symbols.
        
        :param symbols: List of option symbols, separated by commas; maximum 20 symbols per query.
                       Example: "AAPL,TSLA" or ["AAPL", "TSLA"]
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

    def set_timespan(self, timespan):
        """
        Set bar time granularity.
        
        :param timespan: Bar time granularity, e.g., M1, M5, M15, M30, M60, M120, M240, D, W, M, Y
        """
        self.add_query_param("timespan", timespan)

    def set_count(self, count='200'):
        """
        Set number of bars to return.
        
        :param count: Number of bars, default is 200, maximum is 1200.
        """
        self.add_query_param("count", count)

    def set_real_time_required(self, real_time_required):
        """
        Set whether to include the latest data.
        
        :param real_time_required: Whether to include the latest data, default is false.
        """
        if real_time_required is not None:
            self.add_query_param("real_time_required", real_time_required)
