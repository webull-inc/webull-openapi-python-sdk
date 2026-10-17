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

from webull.data.common.category import Category
from webull.data.request.get_news_detail_request import GetNewsDetailRequest
from webull.data.request.get_stock_news_request import GetStockNewsRequest
from webull.data.request.get_news_search_request import GetNewsSearchRequest


class News:
    def __init__(self, api_client):
        self.client = api_client

    def get_news_search(self, keyword, start_date=None, end_date=None, pagination_key=None):
        """
        Search US market news by keyword. US only.

        :param keyword: Search keyword, max 100 characters, required.
        :param start_date: Start date in yyyy-MM-dd format, None defaults to 7 days ago.
        :param end_date: End date in yyyy-MM-dd format, None defaults to today.
        :param pagination_key: Pagination key from the previous page response; not returned on the last page.
        """
        request = GetNewsSearchRequest()
        request.set_keyword(keyword)
        request.set_start_date(start_date)
        request.set_end_date(end_date)
        request.set_pagination_key(pagination_key)
        response = self.client.get_response(request)
        return response

    def get_news_detail(self, news_id):
        """
        Query the full content of a US market news article by its ID. US only.

        :param news_id: News unique identifier, required.
        """
        request = GetNewsDetailRequest()
        request.set_news_id(news_id)
        response = self.client.get_response(request)
        return response

    def get_stock_news(self, symbol, category=Category.US_STOCK.name, sentiment=None, pagination_key=None):
        """
        Query stock-related news list with optional sentiment filter.

        :param symbol: Stock symbol, e.g. TSLA, required.
        :param category: Market category. Supported: US_STOCK (default), HK_STOCK.
        :param sentiment: Sentiment filter: POSITIVE, NEGATIVE or NEUTRAL, None to return all.
        :param pagination_key: Pagination key from the previous page response; not returned on the last page.
        """
        request = GetStockNewsRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_sentiment(sentiment)
        request.set_pagination_key(pagination_key)
        response = self.client.get_response(request)
        return response
