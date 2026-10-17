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
from webull.data.common.contract_type import ContractType
from webull.data.common.timespan import Timespan
from webull.core.client import ApiClient
from webull.data.data_client import DataClient

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"

# The token_dir parameter can be used to specify the directory for storing the 2FA token. Both absolute and relative paths are supported and this option has the highest priority.
# Alternatively, the storage directory can be configured via an environment variable with the key WEBULL_OPENAPI_TOKEN_DIR, which also supports both absolute and relative paths.
# If neither is specified, the default configuration will be used, and the token will be stored at conf/token.txt under the current working directory.
# token_dir = "<your_token_dir>"
# api_client.set_token_dir(token_dir)

api_client = ApiClient(your_app_key, your_app_secret, region_id)
api_client.add_endpoint(region_id, optional_api_endpoint)


if __name__ == '__main__':
    data_client = DataClient(api_client)

    trading_sessions = ["PRE", "RTH", "ATH", "OVN"]
    res = data_client.instrument.get_instrument("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_instrument:', res.json())

    res = data_client.instrument.get_crypto_instrument()
    if res.status_code == 200:
        print('get_crypto_instrument(all):', res.json())

    res = data_client.instrument.get_crypto_instrument("BTCUSD")
    if res.status_code == 200:
        print('get_crypto_instrument:', res.json())

    res = data_client.crypto_market_data.get_crypto_snapshot("BTCUSD")
    if res.status_code == 200:
        print('get_crypto_snapshot:', res.json())

    res = data_client.crypto_market_data.get_crypto_history_bar("BTCUSD", Category.US_CRYPTO.name, Timespan.M1.name)
    if res.status_code == 200:
        print('get_crypto_history_bar:', res.json())

    # Crypto historical bars within a time range using start_time and end_time (timestamps in milliseconds).
    res = data_client.crypto_market_data.get_crypto_history_bar(
        "BTCUSD", Category.US_CRYPTO.name, Timespan.M1.name,
        start_time=1711262998500, end_time=1711349398500)
    if res.status_code == 200:
        print('get_crypto_history_bar with time range:', res.json())

    res = data_client.market_data.get_snapshot('AAPL', Category.US_STOCK.name, extend_hour_required=True, overnight_required=True)
    if res.status_code == 200:
        print('get_snapshot:', res.json())

    # get_history_bar is deprecated: the /market-data/stocks/bars/get endpoint
    # is no longer available. It now delegates to the batch endpoint
    # /market-data/stocks/bars/list. Prefer get_batch_history_bar directly.
    res = data_client.market_data.get_history_bar('AAPL', Category.US_STOCK.name, Timespan.M1.name)
    if res.status_code == 200:
        print('get_history_bar:', res.json())

    res = data_client.market_data.get_batch_history_bar(['AAPL', 'TSLA'], Category.US_STOCK.name, Timespan.M1.name, 1)
    if res.status_code == 200:
        print('get_batch_history_bar:', res.json())

    res = data_client.market_data.get_tick("AAPL", Category.US_STOCK.name, trading_sessions=trading_sessions)
    if res.status_code == 200:
        print('get_tick:', res.json())

    res = data_client.market_data.get_footprint("AAPL", Category.US_STOCK.name, Timespan.S5.name)
    if res.status_code == 200:
        print('get_footprint:', res.json())

    res = data_client.market_data.get_quotes("AAPL", Category.US_STOCK.name, depth=1, overnight_required=True)
    if res.status_code == 200:
        print('get_quotes:', res.json())

    res = data_client.futures_market_data.get_futures_depth("SILZ5", Category.US_FUTURES.name, depth=1)
    if res.status_code == 200:
        print('get_futures_depth:', res.json())

    res = data_client.futures_market_data.get_futures_history_bars('SILZ5,6BM6', Category.US_FUTURES.name, Timespan.M1.name)
    if res.status_code == 200:
        print('get_futures_history_bars:', res.json())

    # Futures historical bars within a time range using start_time and end_time (timestamps in milliseconds).
    res = data_client.futures_market_data.get_futures_history_bars(
        'SILZ5,6BM6', Category.US_FUTURES.name, Timespan.M1.name,
        start_time=1711262998500, end_time=1711349398500)
    if res.status_code == 200:
        print('get_futures_history_bars with time range:', res.json())

    res = data_client.futures_market_data.get_futures_tick("SILZ5", Category.US_FUTURES.name, count=10)
    if res.status_code == 200:
        print('get_futures_tick:', res.json())

    res = data_client.futures_market_data.get_futures_snapshot("SILZ5,6BM6", Category.US_FUTURES.name)
    if res.status_code == 200:
        print('get_futures_snapshot:', res.json())

    res = data_client.futures_market_data.get_futures_footprint("SILZ5,6BM6", Category.US_FUTURES.name, Timespan.S5.name)
    if res.status_code == 200:
        print('get_futures_footprint:', res.json())

    res = data_client.instrument.get_futures_products(Category.US_FUTURES.name)
    if res.status_code == 200:
        print('get_futures_products:', res.json())

    res = data_client.instrument.get_futures_instrument("ESZ5", Category.US_FUTURES.name)
    if res.status_code == 200:
        print('get_futures_instrument:', res.json())

    res = data_client.instrument.get_futures_instrument_by_code("ES", Category.US_FUTURES.name, ContractType.MONTHLY.name)
    if res.status_code == 200:
        print('get_futures_instrument_by_code:', res.json())

    res = data_client.instrument.get_company_profile("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_company_profile:', res.json())

    res = data_client.instrument.get_analyst_target_price("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_analyst_target_price:', res.json())

    res = data_client.instrument.get_analyst_rating("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_analyst_rating:', res.json())

    # NOII (Net Order Imbalance Indicator) - Opening imbalance bars
    res = data_client.market_data.get_noii_bars("AAPL", Category.US_STOCK.name, "PRE_OPEN")
    if res.status_code == 200:
        print('get_noii_bars (opening):', res.json())

    # NOII - Closing imbalance bars
    res = data_client.market_data.get_noii_bars("AAPL", Category.US_STOCK.name, "PRE_CLOSE")
    if res.status_code == 200:
        print('get_noii_bars (closing):', res.json())

    # NOII Snapshot - Opening imbalance
    res = data_client.market_data.get_noii_snapshot("AAPL", Category.US_STOCK.name, "PRE_OPEN")
    if res.status_code == 200:
        print('get_noii_snapshot (opening):', res.json())

    # NOII Snapshot - Closing imbalance
    res = data_client.market_data.get_noii_snapshot("AAPL", Category.US_STOCK.name, "PRE_CLOSE")
    if res.status_code == 200:
        print('get_noii_snapshot (closing):', res.json())

    # Option market data - Historical bars
    # Rate limit: 1 request per second per App Key
    res = data_client.option_market_data.get_option_history_bars('AAPL260522C00300000', Category.US_OPTION.name, Timespan.M1.name)
    if res.status_code == 200:
        print('get_option_history_bars:', res.json())

    # Option historical bars within a time range using start_time and end_time (timestamps in milliseconds).
    res = data_client.option_market_data.get_option_history_bars(
        'AAPL260522C00300000', Category.US_OPTION.name, Timespan.M1.name,
        start_time=1711262998500, end_time=1711349398500)
    if res.status_code == 200:
        print('get_option_history_bars with time range:', res.json())

    # Option market data - Tick
    # Rate limit: 60 requests per minute
    res = data_client.option_market_data.get_option_tick("AAPL260522C00300000", Category.US_OPTION.name, count=30)
    if res.status_code == 200:
        print('get_option_tick:', res.json())

    # Option market data - Snapshot
    # Rate limit: 60 requests per minute
    res = data_client.option_market_data.get_option_snapshot("AAPL260522C00300000", Category.US_OPTION.name)
    if res.status_code == 200:
        print('get_option_snapshot:', res.json())

    # Fundamentals - Capital Flow
    res = data_client.fundamentals.get_capital_flow("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_capital_flow:', res.json())

    # Fundamentals - Industry Comparison
    res = data_client.fundamentals.get_industry_comparison("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_industry_comparison:', res.json())

    # Fundamentals - SEC Filings
    res = data_client.fundamentals.get_sec_filings("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_sec_filings:', res.json())

    # Fundamentals - Earnings Calendar
    res = data_client.fundamentals.get_earnings_calendar("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_earnings_calendar:', res.json())

    # Fundamentals - Dividend Calendar
    res = data_client.fundamentals.get_dividend_calendar("TSLA", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_dividend_calendar:', res.json())

    # Fundamentals - Fund Splits
    res = data_client.fundamentals.get_fund_splits("QQQ", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_fund_splits:', res.json())

    # Fundamentals - Fund Rating
    res = data_client.fundamentals.get_fund_rating("QQQ", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_fund_rating:', res.json())

    # Fundamentals - Fund Performance
    res = data_client.fundamentals.get_fund_performance("QQQ", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_fund_performance:', res.json())

    # Fundamentals - Fund Net Value
    res = data_client.fundamentals.get_fund_net_value("QQQ", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_fund_net_value:', res.json())

    # Fundamentals - Fund Holdings
    res = data_client.fundamentals.get_fund_holdings("QQQ", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_fund_holdings:', res.json())

    # Fundamentals - Fund Files
    res = data_client.fundamentals.get_fund_files("QQQ", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_fund_files:', res.json())

    # Fundamentals - Fund Dividends
    res = data_client.fundamentals.get_fund_dividends("QQQ", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_fund_dividends:', res.json())

    # Fundamentals - Fund Brief
    res = data_client.fundamentals.get_fund_brief("QQQ", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_fund_brief:', res.json())

    # Fundamentals - Fund Allocation
    res = data_client.fundamentals.get_fund_allocation("QQQ", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_fund_allocation:', res.json())

    # Fundamentals - Financials Indicators
    res = data_client.fundamentals.get_financials_indicators("TSLA", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_financials_indicators:', res.json())

    # Fundamentals - Financials Income
    res = data_client.fundamentals.get_financials_income("TSLA", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_financials_income:', res.json())

    # Fundamentals - Financials Cashflow
    res = data_client.fundamentals.get_financials_cashflow("TSLA", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_financials_cashflow:', res.json())

    # Fundamentals - Financials Balance Sheet
    res = data_client.fundamentals.get_financials_balance_sheet("TSLA", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_financials_balance_sheet:', res.json())

    # Fundamentals - Financials Alert
    res = data_client.fundamentals.get_financials_alert("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_financials_alert:', res.json())

    # Fundamentals - Forecast EPS
    res = data_client.fundamentals.get_forecast_eps("AAPL", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_forecast_eps:', res.json())

    # Option Instrument - Query option contracts by underlying symbol and filters
    res = data_client.instrument.get_option_contracts(Category.US_OPTION.name,"AAPL")
    if res.status_code == 200:
        print('get_option_contracts:', res.json())

    # Screener - Market Sectors
    res = data_client.screener.get_market_sectors(Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_market_sectors:', res.json())

    # Screener - Market Sectors Detail
    res = data_client.screener.get_market_sectors_detail("6391", Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_market_sectors_detail:', res.json())

    # Screener - High Dividend Rank
    res = data_client.screener.get_high_dividend(Category.US_STOCK.name)
    if res.status_code == 200:
        print('get_high_dividend:', res.json())

    # Screener - 52 Week High/Low
    res = data_client.screener.get_52whl(Category.US_STOCK.name, rank_type="NEW_HIGH")
    if res.status_code == 200:
        print('get_52whl:', res.json())

    # ==================== Screeners ====================
    # Market sentiment (fear & greed) index
    sentiment_res = data_client.screener.get_fear_and_greed_index(Category.US_STOCK.name)
    if sentiment_res.status_code == 200:
        print('get_fear_and_greed_index:', sentiment_res.json())

    # Stock unusual activities
    unusual_res = data_client.screener.get_stock_unusual_activities("NVDA", Category.US_STOCK.name, count=10)
    if unusual_res.status_code == 200:
        print('get_stock_unusual_activities:', unusual_res.json())

    # ==================== Fundamentals ====================
    # Macro economic calendar
    calendar_res = data_client.fundamentals.get_economic_calendars("US", "2026-09-01", "2026-09-08")
    if calendar_res.status_code == 200:
        print('get_economic_calendars:', calendar_res.json())

    # Institution search -> 13F holdings -> holding changes
    institutions_res = data_client.fundamentals.get_institution_search("Bridgewater")
    if institutions_res.status_code == 200:
        print('get_institution_search:', institutions_res.json())

    holdings_res = data_client.fundamentals.get_institution_holdings("0001738828")
    if holdings_res.status_code == 200:
        print('get_institution_holdings:', holdings_res.json())

    holding_changes_res = data_client.fundamentals.get_institution_holding_changes("0001738828", "OPEN", count=10)
    if holding_changes_res.status_code == 200:
        print('get_institution_holding_changes:', holding_changes_res.json())

    # Insider transactions and holdings overview
    insider_tx_res = data_client.fundamentals.get_insider_transactions("NVDA", Category.US_STOCK.name)
    if insider_tx_res.status_code == 200:
        print('get_insider_transactions:', insider_tx_res.json())

    insider_overview_res = data_client.fundamentals.get_insider_holdings(
        "NVDA", Category.US_STOCK.name, compare_months=1)
    if insider_overview_res.status_code == 200:
        print('get_insider_holdings:', insider_overview_res.json())

    # ==================== News ====================
    # Search news by keyword
    search_news_res = data_client.news.get_news_search("Starlink")
    if search_news_res.status_code == 200:
        print('get_news_search:', search_news_res.json())

    # Stock news list
    stock_news_res = data_client.news.get_stock_news("TSLA", Category.US_STOCK.name)
    if stock_news_res.status_code == 200:
        print('get_stock_news:', stock_news_res.json())

    # News detail (use a news_id returned by the list/search APIs)
    news_items = (stock_news_res.json().get('data') or []) if stock_news_res.status_code == 200 else []
    if news_items:
        news_detail_res = data_client.news.get_news_detail(news_items[0].get('news_id'))
        if news_detail_res.status_code == 200:
            print('get_news_detail:', news_detail_res.json())
