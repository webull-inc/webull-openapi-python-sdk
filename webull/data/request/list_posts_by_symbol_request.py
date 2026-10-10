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


class ListPostsBySymbolRequest(ApiRequest):
    """Request for listing community posts associated with a symbol."""

    def __init__(self):
        ApiRequest.__init__(self, "/market-data/communities/posts/symbols/list", version="v3", method="GET",
                            query_params={})

    def set_symbol(self, symbol):
        """Set the stock symbol."""
        self.add_query_param("symbol", symbol)

    def set_category(self, category):
        """Set the market category."""
        self.add_query_param("category", category)

    def set_keyword(self, keyword):
        """Set the optional search keyword."""
        if keyword is not None:
            self.add_query_param("keyword", keyword)

    def set_pagination_key(self, pagination_key):
        """Set the optional pagination key from the previous response."""
        if pagination_key is not None:
            self.add_query_param("pagination_key", pagination_key)
