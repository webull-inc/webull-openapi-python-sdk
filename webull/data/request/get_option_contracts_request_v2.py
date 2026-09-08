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


class GetOptionContractsRequestV2(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/trading/instruments/options/contracts/list", version="v3", method="GET",
                           query_params={})

    def set_category(self, category):
        self.add_query_param("category", category)

    def set_option_symbols(self, option_symbols):
        if option_symbols:
            self.add_query_param("option_symbols", option_symbols)

    def set_underlying_symbols(self, underlying_symbols):
        if underlying_symbols:
            self.add_query_param("underlying_symbols", underlying_symbols)

    def set_status(self, status):
        if status:
            self.add_query_param("status", status)

    def set_start_date(self, start_date):
        if start_date:
            self.add_query_param("start_date", start_date)

    def set_end_date(self, end_date):
        if end_date:
            self.add_query_param("end_date", end_date)

    def set_root_symbol(self, root_symbol):
        if root_symbol:
            self.add_query_param("root_symbol", root_symbol)

    def set_option_type(self, option_type):
        if option_type:
            self.add_query_param("option_type", option_type)

    def set_style(self, style):
        if style:
            self.add_query_param("style", style)

    def set_strike_price_gte(self, strike_price_gte):
        if strike_price_gte is not None:
            self.add_query_param("strike_price_gte", strike_price_gte)

    def set_strike_price_lte(self, strike_price_lte):
        if strike_price_lte is not None:
            self.add_query_param("strike_price_lte", strike_price_lte)

    def set_ppind(self, ppind):
        if ppind is not None:
            self.add_query_param("ppind", ppind)

    def set_show_deliverables(self, show_deliverables):
        if show_deliverables is not None:
            self.add_query_param("show_deliverables", show_deliverables)

    def set_pagination_key(self, pagination_key):
        if pagination_key:
            self.add_query_param("pagination_key", pagination_key)
