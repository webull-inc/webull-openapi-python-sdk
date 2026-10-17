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


class GetNewsSearchRequest(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/market-data/news/search/list", version='v3', method="GET",
                            query_params={})

    def set_keyword(self, keyword):
        if keyword is not None:
            self.add_query_param("keyword", keyword)

    def set_start_date(self, start_date):
        if start_date:
            self.add_query_param("start_date", start_date)

    def set_end_date(self, end_date):
        if end_date:
            self.add_query_param("end_date", end_date)

    def set_pagination_key(self, pagination_key):
        if pagination_key:
            self.add_query_param("pagination_key", pagination_key)
