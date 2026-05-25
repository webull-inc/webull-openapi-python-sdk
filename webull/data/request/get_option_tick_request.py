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


class GetOptionTickRequest(ApiRequest):
    """
    Request class for querying option tick data.
    Returns detailed tick-by-tick trade records for a specified option code,
    including trade time, price, volume, and trade direction.
    """

    def __init__(self):
        ApiRequest.__init__(self, "/openapi/market-data/option/tick", version='v2', method="GET", query_params={})

    def set_symbol(self, symbol):
        """
        Set option symbol.
        
        :param symbol: Option symbol.
        """
        self.add_query_param("symbol", symbol)

    def set_category(self, category):
        """
        Set security type.
        
        :param category: Security type. Currently only US_OPTION is supported.
        """
        self.add_query_param("category", category)

    def set_count(self, count='30'):
        """
        Set number of ticks to return.
        
        :param count: Number of ticks, default is 30, maximum is 1200.
        """
        self.add_query_param("count", count)
