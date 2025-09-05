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

class GetQuotesRequest(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/market-data/quotes", version='v2', method="GET", query_params={})

    def set_symbol(self, symbol):
        self.add_query_param("symbol", symbol)
    
    def set_category(self, category):
        self.add_query_param("category", category)

    def set_depth(self, depth):
        if depth:
            self.add_query_param("depth", depth)

    def set_overnight_required(self, overnight_required):
        if overnight_required:
            self.add_query_param("overnight_required", overnight_required)