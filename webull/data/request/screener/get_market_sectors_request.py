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


class GetMarketSectorsRequest(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/openapi/market-data/screener/market-sectors", version='v2', method="GET",
                           query_params={})

    def set_category(self, category):
        if category:
            self.add_query_param("category", category)

    def set_agg_type(self, agg_type):
        if agg_type:
            self.add_query_param("agg_type", agg_type)

    def set_period(self, period):
        if period:
            self.add_query_param("period", period)

    def set_page_index(self, page_index):
        if page_index:
            self.add_query_param("page_index", page_index)

    def set_page_size(self, page_size):
        if page_size:
            self.add_query_param("page_size", page_size)

    def set_direction(self, direction):
        if direction:
            self.add_query_param("direction", direction)
