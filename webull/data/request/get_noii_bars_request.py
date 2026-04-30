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


class GetNoiiBarsRequest(ApiRequest):
    """
    Request class for Stock NOII Bars API.
    
    NOII (Net Order Imbalance Indicator) data provides insight into market supply
    and demand during NASDAQ opening and closing auctions.
    """

    def __init__(self):
        ApiRequest.__init__(self, "/openapi/market-data/stock/noii/bars", version="v2", method="GET", query_params={})

    def set_symbol(self, symbol):
        """
        Set the security symbol. Only single symbol query is supported.

        :param symbol: Security symbol, e.g., AAPL
        """
        self.add_query_param("symbol", symbol)

    def set_category(self, category):
        """
        Set the security category. Currently only US_STOCK is supported.

        :param category: Security category, e.g., US_STOCK
        """
        self.add_query_param("category", category)

    def set_imbalance_action_type(self, imbalance_action_type):
        """
        Set the imbalance action type.

        :param imbalance_action_type: Imbalance action type.
            - PRE_OPEN: Opening imbalance
            - PRE_CLOSE: Closing imbalance
        """
        self.add_query_param("imbalance_action_type", imbalance_action_type)
