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

from webull.data.request.screener.get_gainers_losers_request import GetGainersLosersRequest
from webull.data.request.screener.get_most_active_request import GetMostActiveRequest
from webull.data.request.screener.get_market_sectors_request import GetMarketSectorsRequest
from webull.data.request.screener.get_market_sectors_detail_request import GetMarketSectorsDetailRequest
from webull.data.request.screener.get_high_dividend_request import GetHighDividendRequest
from webull.data.request.screener.get_52whl_request import Get52WHLRequest


class Screener:
    """
    Screener class provides access to stock screening and ranking APIs.
    
    This class includes methods for:
    - Top gainers/losers ranking by price change over various time periods
    - Most active stocks ranking by volume, turnover, and other activity metrics
    """
    
    def __init__(self, api_client):
        self.client = api_client

    def get_gainers_losers(self, rank_type, category, sort_by, page_index=None, page_size=None, direction=None):
        """
        Get stock top gainers or losers ranking by price change percentage.
        
        This API returns stocks ranked by price change over different time periods.
        Use direction='DESC' for gainers (top performers) and direction='ASC' for losers.
        
        :param rank_type: Time period for ranking. Required.
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
        :param category: Security market category. Required. (e.g., 'US_STOCK')
        :param sort_by: Secondary sort field. Required.
            Enum values: CHANGE_RATIO, RELATIVE_VOLUME_10D, MARKET_VALUE, CLOSE,
            PRICE, PE_TTM, HIGH, LOW, AMPLITUDE, TURNOVER, VOLUME
        :param page_index: Page number, starting from 1. Optional.
        :param page_size: Number of records per page. Optional.
        :param direction: Sort direction. Optional.
            - ASC: Ascending (for losers)
            - DESC: Descending (for gainers)
        :return: Response containing has_more flag and list of ranked stocks with
            instrument_id, symbol, name, exchange_code, currency_code, pre_close,
            open, high, low, close, price, change, change_ratio, volume,
            turnover, turnover_rate, market_value, amplitude.
        """
        request = GetGainersLosersRequest()
        request.set_rank_type(rank_type)
        request.set_category(category)
        request.set_sort_by(sort_by)
        request.set_page_index(page_index)
        request.set_page_size(page_size)
        request.set_direction(direction)
        response = self.client.get_response(request)
        return response

    def get_most_active(self, category, rank_type=None, sort_by=None, page_index=None, page_size=None, direction=None):
        """
        Get most actively traded stocks ranking.
        
        This API returns stocks ranked by trading activity metrics such as volume,
        relative volume, turnover amount, turnover rate, or amplitude.
        
        Default sort: rank_type=VOLUME, sort_by=VOLUME, direction=DESC
        
        The relative_volume_10d field is unique to this endpoint compared to
        the gainers/losers endpoint.
        
        :param category: Security market category. Required. (e.g., 'US_STOCK')
        :param rank_type: Activity metric for ranking. Optional (defaults to VOLUME).
            Enum values:
            - VOLUME: Trading volume
            - RELATIVE_VOLUME_10D: 10-day relative volume
            - TURNOVER: Turnover amount
            - TURNOVER_RATE: Turnover rate
            - AMPLITUDE: Price amplitude
        :param sort_by: Secondary sort field. Optional.
            Enum values: CHANGE_RATIO, RELATIVE_VOLUME_10D, MARKET_VALUE, CLOSE,
            PRICE, PE_TTM, HIGH, LOW, AMPLITUDE, TURNOVER, VOLUME
        :param page_index: Page number, starting from 1. Optional.
        :param page_size: Number of records per page. Optional.
        :param direction: Sort direction. Optional (defaults to DESC).
            - ASC: Ascending order
            - DESC: Descending order
        :return: Response containing has_more flag and list of ranked stocks with
            instrument_id, symbol, name, exchange_code, currency_code, pre_close,
            open, high, low, close, price, change, change_ratio, volume,
            turnover, turnover_rate, market_value, amplitude, relative_volume_10d.
        """
        request = GetMostActiveRequest()
        request.set_category(category)
        request.set_rank_type(rank_type)
        request.set_sort_by(sort_by)
        request.set_page_index(page_index)
        request.set_page_size(page_size)
        request.set_direction(direction)
        response = self.client.get_response(request)
        return response

    def get_market_sectors(self, category, agg_type=None, period=None, page_index=None, page_size=None, direction=None):
        """
        Get all sector overview data.

        :param category: Security category. Required. (e.g., 'US_STOCK')
        :param agg_type: Statistics type, default is MARKET_VALUE. Enum: MARKET_VALUE, VOLUME.
        :param period: Statistics period, default is D1. Enum: D1, D5, M01, M03.
        :param page_index: Page index.
        :param page_size: Number of records per page.
        :param direction: Sorting direction. Enum: ASC (ascending), DESC (descending).
        """
        request = GetMarketSectorsRequest()
        request.set_category(category)
        request.set_agg_type(agg_type)
        request.set_period(period)
        request.set_page_index(page_index)
        request.set_page_size(page_size)
        request.set_direction(direction)
        response = self.client.get_response(request)
        return response

    def get_market_sectors_detail(self, sector_id, category, period=None, page_index=None, page_size=None, sort_by=None, direction=None):
        """
        Get stock list and statistics for a specific sector.

        :param sector_id: Sector ID. Required.
        :param category: Security category. Required. (e.g., 'US_STOCK')
        :param period: Statistics period, default is D1. Enum: D1, D5, M01, M03.
        :param page_index: Page index.
        :param page_size: Number of records per page.
        :param sort_by: Sort field, default is CHANGE_RATIO. Enum: CHANGE_RATIO, RELATIVE_VOLUME_10D, MARKET_VALUE, CLOSE, PRICE, PE_TTM, HIGH, LOW, AMPLITUDE, TURNOVER, VOLUME, YIELD, DIVIDEND.
        :param direction: Sorting direction. Enum: ASC (ascending), DESC (descending).
        """
        request = GetMarketSectorsDetailRequest()
        request.set_sector_id(sector_id)
        request.set_category(category)
        request.set_period(period)
        request.set_page_index(page_index)
        request.set_page_size(page_size)
        request.set_sort_by(sort_by)
        request.set_direction(direction)
        response = self.client.get_response(request)
        return response

    def get_high_dividend(self, category, sort_by=None, page_index=None, page_size=None, direction=None):
        """
        Get high dividend rank list.

        :param category: Security category. Required. (e.g., 'US_STOCK')
        :param sort_by: Sort field, default is YIELD. Enum: CHANGE_RATIO, RELATIVE_VOLUME_10D, MARKET_VALUE, CLOSE, PRICE, PE_TTM, HIGH, LOW, AMPLITUDE, TURNOVER, VOLUME, YIELD, DIVIDEND.
        :param page_index: Page index.
        :param page_size: Number of records per page.
        :param direction: Sorting direction. Enum: ASC (ascending), DESC (descending).
        """
        request = GetHighDividendRequest()
        request.set_category(category)
        request.set_sort_by(sort_by)
        request.set_page_index(page_index)
        request.set_page_size(page_size)
        request.set_direction(direction)
        response = self.client.get_response(request)
        return response

    def get_52whl(self, category, rank_type=None, sort_by=None, page_index=None, page_size=None, direction=None):
        """
        Get 52 week high/low rank list.

        :param category: Security category. Required. (e.g., 'US_STOCK')
        :param rank_type: Index code. Enum: NEW_HIGH, NEAR_HIGH, NEW_LOW, NEAR_LOW.
        :param sort_by: Sort field, default is CHANGE_RATIO_52W. Enum: CHANGE_RATIO, RELATIVE_VOLUME_10D, MARKET_VALUE, CLOSE, PRICE, PE_TTM, HIGH, LOW, AMPLITUDE, TURNOVER, VOLUME, YIELD, DIVIDEND.
        :param page_index: Page index.
        :param page_size: Number of records per page.
        :param direction: Sorting direction. Enum: ASC (ascending), DESC (descending).
        """
        request = Get52WHLRequest()
        request.set_rank_type(rank_type)
        request.set_category(category)
        request.set_sort_by(sort_by)
        request.set_page_index(page_index)
        request.set_page_size(page_size)
        request.set_direction(direction)
        response = self.client.get_response(request)
        return response
