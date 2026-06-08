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


class GetMostActiveRequest(ApiRequest):
    """
    Request class for Stock Top Active Rank API.
    
    This API returns the most actively traded stocks ranked by volume, relative volume,
    turnover, turnover rate, or amplitude.
    
    Default sort: rank_type=VOLUME, order=VOLUME, direction=DESC
    
    The relative_volume_10d field is unique to the Top Active response compared to
    the Gainers/Losers endpoint.
    """
    
    def __init__(self):
        ApiRequest.__init__(self, "/openapi/market-data/screener/top-active", version="v2", method="GET", query_params={})

    def set_rank_type(self, rank_type):
        """
        Set the ranking dimension that determines which activity metric is used for filtering.
        
        :param rank_type: Activity metric for ranking. Optional (defaults to VOLUME).
            Enum values:
            - VOLUME: Trading volume
            - RELATIVE_VOLUME_10D: 10-day relative volume
            - TURNOVER: Turnover amount
            - TURNOVER_RATE: Turnover rate
            - AMPLITUDE: Price amplitude
        """
        if rank_type is not None:
            self.add_query_param("rank_type", rank_type)

    def set_category(self, category):
        """
        Set the security market category.

        :param category: Security market category. Required.
            Enum values: US_STOCK
        """
        if category is not None:
            self.add_query_param("category", category)

    def set_sort_by(self, sort_by):
        """
        Set the secondary sort field for further ordering within the ranking.
        
        :param sort_by: Sort field. Optional.
            Enum values:
            - CHANGE_RATIO: Price change percentage
            - RELATIVE_VOLUME_10D: 10-day relative volume
            - MARKET_VALUE: Market capitalization
            - CLOSE: Closing price
            - PRICE: Current price
            - PE_TTM: Trailing twelve months P/E ratio
            - HIGH: Intraday high
            - LOW: Intraday low
            - AMPLITUDE: Price amplitude
            - TURNOVER: Turnover amount
            - VOLUME: Trading volume
        """
        if sort_by is not None:
            self.add_query_param("sort_by", sort_by)

    def set_page_index(self, page_index):
        """
        Set the page number for pagination.
        
        :param page_index: Page number, starting from 1. Optional.
        """
        if page_index is not None:
            self.add_query_param("page_index", page_index)

    def set_page_size(self, page_size):
        """
        Set the number of records per page.
        
        :param page_size: Number of records returned per page. Optional.
        """
        if page_size is not None:
            self.add_query_param("page_size", page_size)

    def set_direction(self, direction):
        """
        Set the sort direction.
        
        :param direction: Sort direction. Optional (defaults to DESC).
            Enum values:
            - ASC: Ascending order
            - DESC: Descending order
        """
        if direction is not None:
            self.add_query_param("direction", direction)
