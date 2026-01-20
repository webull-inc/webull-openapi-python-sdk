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

import logging
import sys

from webull.core.http.initializer.client_initializer import ClientInitializer
from webull.data.quotes.crypto_market_data import CryptoMarketData
from webull.data.quotes.event_market_data import EventMarketData
from webull.data.quotes.futures_market_data import FuturesMarketData
from webull.data.quotes.instrument import Instrument
from webull.data.quotes.market_data import MarketData


class DataClient:
    def __init__(self, api_client):
        self._init_logger(api_client)
        ClientInitializer.initializer(api_client)
        self.instrument = Instrument(api_client)
        self.market_data = MarketData(api_client)
        self.crypto_market_data = CryptoMarketData(api_client)
        self.futures_market_data = FuturesMarketData(api_client)
        self.event_market_data = EventMarketData(api_client)

    def _init_logger(self, api_client):
        # No logger configured, using default console and local file logging.
        if not getattr(api_client, '_stream_logger_set', False) and not getattr(api_client, '_file_logger_set', False):
            log_format = '%(thread)d %(asctime)s %(name)s %(levelname)s %(message)s'
            log_file_path = 'webull_data_sdk.log'
            api_client.set_stream_logger(stream=sys.stdout, format_string=log_format)
            api_client.set_file_logger(path=log_file_path, log_level=logging.INFO, format_string=log_format)