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
from webull.data.common.category import Category
from webull.data.request.get_batch_historical_bars_request import BatchHistoricalBarsRequest
from webull.data.request.get_corp_action_request import GetCorpActionRequest
from webull.data.request.get_eod_bars_request import GetEodBarsRequest
from webull.data.request.get_footprint_request import GetFootprintRequest
from webull.data.request.get_historical_bars_request import GetHistoricalBarsRequest
from webull.data.request.get_quotes_request import GetQuotesRequest
from webull.data.request.get_snapshot_request import GetSnapshotRequest
from webull.data.request.get_tick_request import GetTickRequest


class MarketData:
    def __init__(self, api_client):
        self.client = api_client

    def get_history_bar(self, symbol, category, timespan, count='200', real_time_required=None, trading_sessions=None):
        """
        Returns to Instrument in the window aggregated data.
        According to the last N K-lines of the stock code, it supports various granularity K-lines such as m1 and m5.
        Currently, only the K-line with the previous weight is provided for the daily K-line and above,
        and only the un-weighted K-line is provided for the minute K.

        :param symbol: Securities code
        :param category: Security type, enumeration.
        :param timespan: K-line time granularity
        :param count: The number of lines: the default is 200, and the maximum limit is 1200
        :param real_time_required: Returns the latest trade quote data. By default, the most recent market data is returned.
        :param trading_sessions: Specify trading session, multiple selections are allowed
        By default, only intraday candlestick data is returned.
        """
        history_bar_request = GetHistoricalBarsRequest()
        history_bar_request.set_symbol(symbol)
        history_bar_request.set_category(category)
        history_bar_request.set_timespan(timespan)
        history_bar_request.set_count(count)
        history_bar_request.set_real_time_required(real_time_required)
        history_bar_request.set_trading_sessions(trading_sessions)
        response = self.client.get_response(history_bar_request)
        return response

    def get_batch_history_bar(self, symbols, category, timespan, count='200', real_time_required=None, trading_sessions=None):
        """
        Batch query K-line data for multiple symbols, returning aggregated data within the window.
        According to the last N K-lines of the stock code, it supports various granularity K-lines such as m1 and m5.
        Currently, only the K-line with the previous weight is provided for the daily K-line and above,
        and only the un-weighted K-line is provided for the minute K.

        :param symbols: List of security codes
        :param category: Security type, enumeration
        :param timespan: K-line interval
        :param count: Number of K-lines to return, default is 200, maximum is 1200
        :param real_time_required: Returns the latest trade quote data. By default, the most recent market data is returned.
        :param trading_sessions: Specify trading session, multiple selections are allowed
        By default, only intraday candlestick data is returned.
        """
        history_bar_request = BatchHistoricalBarsRequest()
        history_bar_request.set_symbols(symbols)
        history_bar_request.set_category(category)
        history_bar_request.set_timespan(timespan)
        history_bar_request.set_count(count)
        history_bar_request.set_real_time_required(real_time_required)
        history_bar_request.set_trading_sessions(trading_sessions)
        response = self.client.get_response(history_bar_request)
        return response

    def get_snapshot(self, symbols, category, extend_hour_required=None, overnight_required=None):
        """
        Query the latest stock market snapshots in batches according to the stock code list.

        :param symbols: List of security codes; for example: single: 00700 multiple: 00700,00981;
        For each request,up to 100 symbols can be subscribed; Under the authority of Hong Kong stock BMP,
        a single request supports up to 20 symbols
        :param category: Security type, enumeration.
        :param extend_hour_required: Whether to include pre-market and after-hours sessions, the default is not included
        :param overnight_required: Whether to include the night session, the default is not included
        """
        snapshot_request = GetSnapshotRequest()
        snapshot_request.set_symbols(symbols)
        snapshot_request.set_category(category)
        snapshot_request.set_extend_hour_required(extend_hour_required)
        snapshot_request.set_overnight_required(overnight_required)
        response = self.client.get_response(snapshot_request)
        return response

    def get_quotes(self, symbol, category, depth=None, overnight_required=None):
        """
        Query the depth quote of securities according to the stock code list.

        :param symbol: Securities code
        :param category: Security type, enumeration.
        :param depth: Retrieve bid/ask depth
        Level 1 contains only the top 1 bid/ask level.
        Level 2 becomes effective, with 10 levels by default. For U.S. stocks, Level 2 supports up to 50 levels.
        :param overnight_required: Whether to include the night session, the default is not included
        """
        quote_request = GetQuotesRequest()
        quote_request.set_symbol(symbol)
        quote_request.set_category(category)
        quote_request.set_depth(depth)
        quote_request.set_overnight_required(overnight_required)
        response = self.client.get_response(quote_request)
        return response

    def get_tick(self, symbol, category, count='200', trading_sessions=None):
        """
        Query tick-by-tick transaction of securities according to the stock code list.

        :param symbol: Securities code
        :param category: Security type, enumeration.
        :param count: The number of lines: the default is 30, and the maximum limit is 1000
        :param trading_sessions: Specify trading session, multiple selections are allowed
        """
        tick_request = GetTickRequest()
        tick_request.set_symbol(symbol)
        tick_request.set_category(category)
        tick_request.set_count(count)
        tick_request.set_trading_sessions(trading_sessions)
        response = self.client.get_response(tick_request)
        return response

    def get_eod_bar(self, instrument_ids, date=None, count='1'):
        """
        Only for Webull JP

        Query end-of-day market information according to instrument_id.

        :param instrument_ids: Instrument id collection, such as: 913256135,913303964.
        Multiple instrument_ids should be separated by ,.
        A single query supports up to 200 instrument_id
        :param date: UTC time. Time format: yyyy-MM-dd, and the default check is conducted on the latest date
        :param count: With “date” as the deadline, the end-of-day market data of the last “count” trading days:
        the default is 1, and the maximum limit is 800
        """
        eod_bar_request = GetEodBarsRequest()
        eod_bar_request.set_instrument_ids(instrument_ids)
        if date is not None:
            eod_bar_request.set_date(date)
        eod_bar_request.set_count(count)
        response = self.client.get_response(eod_bar_request)
        return response

    def get_corp_action(self, instrument_ids, event_types, start_date=None, end_date=None, page_number=None,
                        page_size=None, last_update_time=None):
        """
        Only for Webull JP
        Supports the query of the corporate events for stock splits and reverse stock split,
        including past and upcoming events.

        :param instrument_ids: Instrument id collection, such as: 913256135,913303964.
        Multiple instrument_ids should be separated by ,.
        A single query supports up to 100 instrument_id
        :param event_types: Event type collection. Multiple event_types should be separated by ,
        :param start_date: Event start date, UTC time.Time format: yyyy-MM-dd
        :param end_date: Event end date, UTC time.Time format: yyyy-MM-dd
        :param page_number: The initial value, if not passed, the first page will be searched by default
        :param page_size: Number of entries per page: default value is 20, and maximum value is 200.
        Integers can be filled
        :param last_update_time: Incremental update time, UTC time. Time format: yyyy-MM-dd HH:mm:ss
        """
        eod_corp_action_request = GetCorpActionRequest()
        eod_corp_action_request.set_instrument_ids(instrument_ids)
        eod_corp_action_request.set_event_types(event_types)
        if start_date is not None:
            eod_corp_action_request.set_start_date(start_date)
        if end_date is not None:
            eod_corp_action_request.set_end_date(end_date)
        if page_number is not None:
            eod_corp_action_request.set_page_number(page_number)
        if page_size is not None:
            eod_corp_action_request.set_page_size(page_size)
        if last_update_time is not None:
            eod_corp_action_request.set_last_update_time(last_update_time)
        response = self.client.get_response(eod_corp_action_request)
        return response

    def get_footprint(self, symbols, category, timespan, count=None,
                      real_time_required=None, trading_sessions=None):
        """
         Search the footprint based on the list of security codes and security types.

        :param symbols: Securities symbol, such as: 00700,00981.
        :param category: Security type, enumeration.
        :param timespan: Time granularity.
        :param count: Number of entries: 200 by default, maximum 1200.
        :param real_time_required: Whether to include the latest data or candlestick charts that are not yet finalized. The default is false, meaning they are not included. This option is only used for minute candlestick charts.
        :param trading_sessions: RTH: During trading hours, PRE: Before trading hours, ATH: After trading hours. Default: RTH.
        """
        footprint_request = GetFootprintRequest()
        footprint_request.set_symbols(symbols)
        footprint_request.set_category(category)
        footprint_request.set_timespan(timespan)
        footprint_request.set_count(count)
        footprint_request.set_real_time_required(real_time_required)
        footprint_request.set_trading_sessions(trading_sessions)
        response = self.client.get_response(footprint_request)
        return response
