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
from webull.data.request.get_capital_flow_request import GetCapitalFlowRequest
from webull.data.request.get_industry_comparison_request import GetIndustryComparisonRequest
from webull.data.request.get_sec_filings_request import GetSecFilingsRequest
from webull.data.request.get_earnings_calendar_request import GetEarningsCalendarRequest
from webull.data.request.get_dividend_calendar_request import GetDividendCalendarRequest
from webull.data.request.get_fund_splits_request import GetFundSplitsRequest
from webull.data.request.get_fund_rating_request import GetFundRatingRequest
from webull.data.request.get_fund_performance_request import GetFundPerformanceRequest
from webull.data.request.get_fund_net_value_request import GetFundNetValueRequest
from webull.data.request.get_fund_holdings_request import GetFundHoldingsRequest
from webull.data.request.get_fund_files_request import GetFundFilesRequest
from webull.data.request.get_fund_dividends_request import GetFundDividendsRequest
from webull.data.request.get_fund_dividends_request_v2 import GetFundDividendsRequestV2
from webull.data.request.get_fund_brief_request import GetFundBriefRequest
from webull.data.request.get_fund_allocation_request import GetFundAllocationRequest
from webull.data.request.get_financials_indicators_request import GetFinancialsIndicatorsRequest
from webull.data.request.get_financials_income_request import GetFinancialsIncomeRequest
from webull.data.request.get_financials_cashflow_request import GetFinancialsCashflowRequest
from webull.data.request.get_financials_balance_sheet_request import GetFinancialsBalanceSheetRequest
from webull.data.request.get_financials_alert_request import GetFinancialsAlertRequest
from webull.data.request.get_forecast_eps_request import GetForecastEpsRequest
from webull.data.request.get_institution_search_request import GetInstitutionSearchRequest
from webull.data.request.get_institution_holdings_request import GetInstitutionHoldingsRequest
from webull.data.request.get_institution_holding_changes_request import GetInstitutionHoldingChangesRequest
from webull.data.request.get_insider_transactions_request import GetInsiderTransactionsRequest
from webull.data.request.get_insider_holdings_request import GetInsiderHoldingsRequest
from webull.data.request.get_economic_calendar_request import GetEconomicCalendarRequest


class Fundamentals:
    def __init__(self, api_client):
        self.client = api_client

    def get_capital_flow(self, symbol, category=Category.US_STOCK.name, count=None):
        """
        Query the capital flow distribution for a stock.

        :param symbol: Security symbol, e.g. AAPL, TSLA.
        :param category: Security type. Supported: US_STOCK, HK_STOCK, CN_STOCK, JP_STOCK.
        :param count: Number of distribution records (default 5), range 1-5.
        """
        request = GetCapitalFlowRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_count(count)
        response = self.client.get_response(request)
        return response

    def get_industry_comparison(self, symbol, category=Category.US_STOCK.name, sort_by=None):
        """
        Query industry comparison data for a stock. Shows up to 20 stocks in the same industry, including the target stock.

        :param symbol: Security symbol, e.g. AAPL, TSLA.
        :param category: Security type. Supported: US_STOCK, HK_STOCK, CN_STOCK.
        :param sort_by: Sort by a certain type. Default: EPS_TTM. Options: EPS_TTM, NAPS, DPS_TTM, ROE, DEBT_TO_ASSETS, NET_MARGIN, DIV_YIELD_TTM, PE_TTM, PB_RATIO.
        """
        request = GetIndustryComparisonRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_sort_by(sort_by)
        response = self.client.get_response(request)
        return response

    def get_sec_filings(self, symbol, category=Category.US_STOCK.name):
        """
        Query SEC filings for a stock. Only supports US stocks. Returns data within the last 3 years.

        :param symbol: Security symbol, e.g. AAPL, TSLA.
        :param category: Security type. Only supports US_STOCK.
        """
        request = GetSecFilingsRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_earnings_calendar(self, symbol, category=Category.US_STOCK.name):
        """
        Query earnings calendar for a stock. Returns earnings reports within half a year before and after the current date.
        Sorted by date in ascending order (oldest to newest).
        Use eps_actual to distinguish published reports (has eps_actual value) from upcoming ones (no eps_actual value).

        :param symbol: Security symbol, e.g. AAPL, TSLA.
        :param category: Security type. Supported: US_STOCK, HK_STOCK, CN_STOCK, JP_STOCK.
        """
        request = GetEarningsCalendarRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_dividend_calendar(self, symbol, category=Category.US_STOCK.name):
        """
        Query dividend calendar for a stock. Returns dividends within half a year before and after the current date.
        Sorted by date in ascending order (oldest to newest).

        :param symbol: Security symbol, e.g. AAPL, TSLA.
        :param category: Security type. Supported: US_STOCK, HK_STOCK, CN_STOCK, JP_STOCK.
        """
        request = GetDividendCalendarRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_fund_splits(self, symbol, category=Category.US_STOCK.name):
        """
        Query fund splits for a stock.

        :param symbol: Security symbol, e.g. QQQ.
        :param category: Security type. Category values are as shown in the enum.
        """
        request = GetFundSplitsRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_fund_rating(self, symbol, category=Category.US_STOCK.name):
        """
        Query fund rating for a security.

        :param symbol: Security symbol, e.g. QQQ.
        :param category: Security type. Category values are as shown in the enum.
        """
        request = GetFundRatingRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_fund_performance(self, symbol, category=Category.US_STOCK.name):
        """
        Query fund performance for a security.

        :param symbol: Security symbol, e.g. QQQ.
        :param category: Security type. Category values are as shown in the enum.
        """
        request = GetFundPerformanceRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_fund_net_value(self, symbol, category=Category.US_STOCK.name, last_date=None, count=None):
        """
        Query fund net value for a security.

        :param symbol: Security symbol, e.g. QQQ.
        :param category: Security type. Category values are as shown in the enum.
        :param last_date: Last query date, e.g. 2026-04-01.
        :param count: The number of each query, default 5, maximum 20.
        """
        request = GetFundNetValueRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_last_date(last_date)
        request.set_count(count)
        response = self.client.get_response(request)
        return response

    def get_fund_holdings(self, symbol, category=Category.US_STOCK.name):
        """
        Query fund top 10 holdings.

        :param symbol: Security symbol, e.g. QQQ.
        :param category: Security type. Category values are as shown in the enum.
        """
        request = GetFundHoldingsRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_fund_files(self, symbol, category=Category.US_STOCK.name):
        """
        Query fund files for a security.

        :param symbol: Security symbol, e.g. QQQ.
        :param category: Security type. Category values are as shown in the enum.
        """
        request = GetFundFilesRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_fund_dividends(self, symbol, category=Category.US_STOCK.name, page_index=None, page_size=None):
        """
        .. deprecated::
            Use :meth:`list_fund_dividends` instead.

        Query fund dividends for a security.

        :param symbol: Security symbol, e.g. QQQ.
        :param category: Security type. Category values are as shown in the enum.
        :param page_index: Page index, default 1. If not passed, the first page will be searched by default.
        :param page_size: Number of entries per page, default 10, maximum 20.
        """
        request = GetFundDividendsRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_page_index(page_index)
        request.set_page_size(page_size)
        response = self.client.get_response(request)
        return response

    def list_fund_dividends(self, symbol, category=Category.US_STOCK.name, pagination_key=None):
        """
        Query fund dividends for a security.

        :param symbol: Security symbol, e.g. QQQ.
        :param category: Security type. Category values are as shown in the enum.
        :param pagination_key: Pagination key from the previous page response; not returned on the last page.
        """
        request = GetFundDividendsRequestV2()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_pagination_key(pagination_key)
        response = self.client.get_response(request)
        return response

    def get_fund_brief(self, symbol, category=Category.US_STOCK.name):
        """
        Query fund brief information.

        :param symbol: Security symbol, e.g. QQQ.
        :param category: Security type. Category values are as shown in the enum.
        """
        request = GetFundBriefRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_fund_allocation(self, symbol, category=Category.US_STOCK.name):
        """
        Query fund asset allocation.

        :param symbol: Security symbol, e.g. QQQ.
        :param category: Security type. Category values are as shown in the enum.
        """
        request = GetFundAllocationRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_financials_indicators(self, symbol, category=Category.US_STOCK.name, type=None, count=None):
        """
        Query financials indicators for a stock.

        :param symbol: Security symbol, e.g. TSLA.
        :param category: Security type. Category values are as shown in the enum.
        :param type: Financial type, default QUARTERLY. Options: ANNUAL, QUARTERLY.
        :param count: The number of each query, default 5, maximum 20.
        """
        request = GetFinancialsIndicatorsRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_type(type)
        request.set_count(count)
        response = self.client.get_response(request)
        return response

    def get_financials_income(self, symbol, category=Category.US_STOCK.name, type=None, count=None):
        """
        Query financials income statement for a stock.

        :param symbol: Security symbol, e.g. TSLA.
        :param category: Security type. Category values are as shown in the enum.
        :param type: Financial type, default QUARTERLY. Options: ANNUAL, QUARTERLY.
        :param count: The number of each query, default 5, maximum 20.
        """
        request = GetFinancialsIncomeRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_type(type)
        request.set_count(count)
        response = self.client.get_response(request)
        return response

    def get_financials_cashflow(self, symbol, category=Category.US_STOCK.name, type=None, count=None):
        """
        Query financials cashflow statement for a stock.

        :param symbol: Security symbol, e.g. TSLA.
        :param category: Security type. Category values are as shown in the enum.
        :param type: Financial type, default QUARTERLY. Options: ANNUAL, QUARTERLY.
        :param count: The number of each query, default 5, maximum 20.
        """
        request = GetFinancialsCashflowRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_type(type)
        request.set_count(count)
        response = self.client.get_response(request)
        return response

    def get_financials_balance_sheet(self, symbol, category=Category.US_STOCK.name, type=None, count=None):
        """
        Query financials balance sheet for a stock.

        :param symbol: Security symbol, e.g. TSLA.
        :param category: Security type. Category values are as shown in the enum.
        :param type: Financial type, default QUARTERLY. Options: ANNUAL, QUARTERLY.
        :param count: The number of each query, default 5, maximum 20.
        """
        request = GetFinancialsBalanceSheetRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_type(type)
        request.set_count(count)
        response = self.client.get_response(request)
        return response

    def get_financials_alert(self, symbol, category=Category.US_STOCK.name):
        """
        Query financials alert for a stock.

        :param symbol: Security symbol, e.g. TSLA.
        :param category: Security type. Category values are as shown in the enum.
        """
        request = GetFinancialsAlertRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_forecast_eps(self, symbol, category=Category.US_STOCK.name):
        """
        Query forecast EPS for a stock. Returns the historical actual EPS of the most recent four disclosed
        fiscal periods, plus the latest analyst consensus forecast EPS (if available).
        Sorted by time in ascending order, returns up to 5 records.

        :param symbol: Security symbol, e.g. AAPL. Only supports a single symbol.
        :param category: Security type. Supported: US_STOCK, HK_STOCK, CN_STOCK.
        """
        request = GetForecastEpsRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        response = self.client.get_response(request)
        return response

    def get_institution_search(self, keyword, pagination_key=None):
        """
        Search US institutional investors by name or SEC CIK number. US only.

        :param keyword: Search keyword (institution name or CIK), required.
        :param pagination_key: Pagination key from the previous page response; not returned on the last page.
        """
        request = GetInstitutionSearchRequest()
        request.set_keyword(keyword)
        request.set_pagination_key(pagination_key)
        response = self.client.get_response(request)
        return response

    def get_institution_holdings(self, cik, pagination_key=None):
        """
        Query a US institution's 13F holdings. US only.

        :param cik: Institution CIK number, required.
        :param pagination_key: Pagination key from the previous page response; not returned on the last page.
        """
        request = GetInstitutionHoldingsRequest()
        request.set_cik(cik)
        request.set_pagination_key(pagination_key)
        response = self.client.get_response(request)
        return response

    def get_institution_holding_changes(self, cik, position, count=None, pagination_key=None):
        """
        Query US institutional holding changes filtered by position type. US only.

        :param cik: Fund CIK number, required.
        :param position: Position type: OPEN, CLOSE, or CHANGE, required.
        :param count: Page size, optional, default 10, max 50.
        :param pagination_key: Pagination key from the previous page response; not returned on the last page.
        """
        request = GetInstitutionHoldingChangesRequest()
        request.set_cik(cik)
        request.set_position(position)
        request.set_count(count)
        request.set_pagination_key(pagination_key)
        response = self.client.get_response(request)
        return response

    def get_insider_transactions(self, symbol, category=Category.US_STOCK.name, side=None, pagination_key=None):
        """
        Query insider transaction records for a stock.

        :param symbol: Stock symbol, e.g. NVDA, required.
        :param category: Market category. Supported: US_STOCK (default), HK_STOCK.
        :param side: Transaction side filter: BUY or SELL, None to return all.
        :param pagination_key: Pagination key from the previous page response; not returned on the last page.
        """
        request = GetInsiderTransactionsRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_side(side)
        request.set_pagination_key(pagination_key)
        response = self.client.get_response(request)
        return response

    def get_insider_holdings(self, symbol, category=Category.US_STOCK.name, compare_months=None):
        """
        Query the insider ownership statistics overview for a stock.

        :param symbol: Stock symbol, e.g. NVDA, required.
        :param category: Market category. Supported: US_STOCK (default), HK_STOCK.
        :param compare_months: Comparison period in months: 1 (default) or 3.
        """
        request = GetInsiderHoldingsRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_compare_months(compare_months)
        response = self.client.get_response(request)
        return response

    def get_economic_calendars(self, region=None, start_date=None, end_date=None, pagination_key=None):
        """
        Query the macroeconomic event calendar for an optional region and date range.
        Results are cursor-paginated, up to 30 events per page.

        :param region: Region code: US (default), CN, EU, JP, GB.
        :param start_date: Start date in yyyy-MM-dd format, None defaults to today.
        :param end_date: End date in yyyy-MM-dd format, None defaults to start date + 7 days.
        :param pagination_key: Pagination key from the previous page response; not returned on the last page.
        """
        request = GetEconomicCalendarRequest()
        request.set_region(region)
        request.set_start_date(start_date)
        request.set_end_date(end_date)
        request.set_pagination_key(pagination_key)
        response = self.client.get_response(request)
        return response
