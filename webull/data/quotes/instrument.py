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
from webull.data.request.get_event_instrument_request import GetEventInstrumentRequest
from webull.data.request.get_event_series_request import GetEventSeriesRequest
from webull.data.request.get_instruments_request import GetInstrumentsRequest
from webull.data.request.get_crypto_instruments_request import GetCryptoInstrumentsRequest
from webull.data.request.get_futures_instruments_request import GetFuturesInstrumentsRequest
from webull.data.request.get_futures_products_request import GetFuturesProductsRequest
from webull.data.request.get_futures_instruments_by_code_request import GetFuturesInstrumentsByCodeRequest


class Instrument:
    def __init__(self, api_client):
        self.client = api_client

    def get_instrument(self, symbols=None, category=Category.US_STOCK.name, status=None, last_instrument_id=None,
                       page_size=1000):
        """
         Query the underlying information according to the security symbol list and security type.

        :param symbols: Securities symbol, such as: 00700,00981.
        :param category: Security type, enumeration.
        :param status: Tradable status.
        :param last_instrument_id: Last instrument id for pagination.
        :param page_size: Page size, default 1000.
        """
        instruments_request = GetInstrumentsRequest()
        instruments_request.set_symbols(symbols)
        instruments_request.set_category(category)
        instruments_request.set_status(status)
        instruments_request.set_last_instrument_id(last_instrument_id)
        instruments_request.set_page_size(page_size)
        response = self.client.get_response(instruments_request)
        return response

    def get_crypto_instrument(self, symbols=None, status=None, last_instrument_id=None,
                              category=Category.US_CRYPTO.name, page_size=1000):
        """
         Query the crypto underlying information according to the security symbol.
        :param symbols: Securities symbol, such as: BTCUSD,ETHUSD.
        :param status: Tradable status.
        :param last_instrument_id: Last instrument id for pagination.
        :param category: (str, required) Instrument type.
                     Possible values: ["US_CRYPTO"]
                     Example: "US_CRYPTO"
        :param page_size: Page size, default 1000.
        """
        crypto_instruments_request = GetCryptoInstrumentsRequest()
        crypto_instruments_request.set_symbols(symbols)
        crypto_instruments_request.set_category(category)
        crypto_instruments_request.set_status(status)
        crypto_instruments_request.set_last_instrument_id(last_instrument_id)
        crypto_instruments_request.set_page_size(page_size)
        response = self.client.get_response(crypto_instruments_request)
        return response

    def get_futures_instrument(self, symbols, category):
        """
         Query the futures instrument information based on the futures contract symbol.

        :param symbols: Futures contract symbol, such as: ESmain,ESM5.
        :param category: Security type, enumeration.
        """

        futures_instrument_request = GetFuturesInstrumentsRequest()
        futures_instrument_request.set_symbols(symbols)
        futures_instrument_request.set_category(category)
        response = self.client.get_response(futures_instrument_request)
        return response

    def get_futures_products(self, category):
        """
        Query futures contract codes in batches based on security types.

        :param category: Security type, enumeration.
        """

        batch_futures_products_request = GetFuturesProductsRequest()
        batch_futures_products_request.set_category(category)
        response = self.client.get_response(batch_futures_products_request)
        return response

    def get_futures_instrument_by_code(self, code, category, contract_type=None):
        """
        Query futures instrument information based on futures contract code.

        :param code: Futures contract code, such as: ES.
        :param category: Security type, enumeration.
        :param contract_type: Contract type, values include
            - MONTHLY: Regular monthly contract
            - MAIN: Main continuous contract
        """

        futures_instrument_request = GetFuturesInstrumentsByCodeRequest()
        futures_instrument_request.set_codes(code)
        futures_instrument_request.set_category(category)
        if contract_type:
            futures_instrument_request.set_contract_type(contract_type)
        response = self.client.get_response(futures_instrument_request)
        return response

    def get_event_series(self, category, last_instrument_id=None, page_size=500):
        """
        Retrieve multiple series with specified filters.
        A series represents a template for recurring events that follow the same format and rules (e.g., “Monthly Jobs Report” ).
        This endpoint allows you to browse and discover available series templates by category.

        :param category: The category which this series belongs to.Allowed values:
                        ECONOMICS, FINANCIALS, POLITICS, ENTERTAINMENT, SCIENCE_TECHNOLOGY,
                        CLIMATE_WEATHER, TRANSPORTATION, CRYPTO, SPORTS
        :param last_instrument_id: Last series id for pagination.
        :param page_size: Page size, default 500.
        """

        event_series_request = GetEventSeriesRequest()
        event_series_request.set_category(category)
        if last_instrument_id:
            event_series_request.set_last_instrument_id(last_instrument_id)
        event_series_request.set_page_size(page_size)
        response = self.client.get_response(event_series_request)
        return response

    def get_event_instrument(self, series_symbol, expiration_date_after=None, last_instrument_id=None, page_size=500):
        """
        Retrieve profile information for event contract markets based on the series symbol.

        :param series_symbol: Symbol that identifies this series.
        :param expiration_date_after: Used to filter items whose expiration date is later than a specified date; the default selection is the current day (inclusive).
        :param last_instrument_id: Last series id for pagination.
        :param page_size: Page size, default 500.
        """

        event_instrument_request = GetEventInstrumentRequest()
        event_instrument_request.set_series_symbol(series_symbol)
        if expiration_date_after:
            event_instrument_request.set_expiration_date_after(expiration_date_after)
        if last_instrument_id:
            event_instrument_request.set_last_instrument_id(last_instrument_id)
        event_instrument_request.set_page_size(page_size)
        response = self.client.get_response(event_instrument_request)
        return response