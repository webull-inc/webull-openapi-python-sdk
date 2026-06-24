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


class GetMarketSectorsDetailRequest(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/openapi/market-data/screener/market-sectors-detail", version='v2', method="GET",
                           query_params={})

    def set_sector_id(self, sector_id):
        if sector_id:
            self.add_query_param("sector_id", sector_id)

    def set_category(self, category):
        if category:
            self.add_query_param("category", category)

    def set_period(self, period):
        if period:
            self.add_query_param("period", period)

    def set_page_index(self, page_index):
        if page_index:
            self.add_query_param("page_index", page_index)

    def set_page_size(self, page_size):
        if page_size:
            self.add_query_param("page_size", page_size)

    def set_sort_by(self, sort_by):
        if sort_by:
            self.add_query_param("sort_by", sort_by)

    def set_direction(self, direction):
        if direction:
            self.add_query_param("direction", direction)
