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


class GetGainersLosersRequestV2(ApiRequest):
    """
    Request class for Stock Top Gainers/Losers Rank API.

    This API returns stocks ranked by price change percentage over different time periods.
    Use direction=DESC for gainers (top performers) and direction=ASC for losers (worst performers).

    The ranking is not paginated and returns the top 200 results.
    """

    def __init__(self):
        ApiRequest.__init__(self, "/market-data/screeners/gainers-losers/list", version="v3", method="GET",
                            query_params={})

    def set_rank_type(self, rank_type):
        """
        Set the ranking time dimension.

        :param rank_type: Time period for ranking. Optional (defaults to DAY_1).
            Enum values:
            - PRE_MARKET: Pre-market session
            - AFTER_MARKET: After-market session
            - MIN_3: 3 minutes
            - MIN_5: 5 minutes
            - DAY_1: 1 day
            - DAY_5: 5 days
            - MONTH_1: 1 month
            - MONTH_3: 3 months
            - WEEK_52: 52 weeks
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

        :param sort_by: Sort field. Optional (defaults to CHANGE_RATIO).
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

    def set_direction(self, direction):
        """
        Set the sort direction.

        :param direction: Sort direction. Optional (defaults to DESC).
            Enum values:
            - ASC: Ascending order (for losers/worst performers)
            - DESC: Descending order (for gainers/top performers)
        """
        if direction is not None:
            self.add_query_param("direction", direction)
