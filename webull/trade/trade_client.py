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
import logging
import sys

from webull.core.http.initializer.client_initializer import ClientInitializer
from webull.trade.trade.account_info import Account
from webull.trade.trade.order_operation import OrderOperation
from webull.trade.trade.trade_calendar import TradeCalendar
from webull.trade.trade.trade_instrument import TradeInstrument
from webull.trade.trade.v2.account_info_v2 import AccountV2
from webull.trade.trade.v2.order_operation_v2 import OrderOperationV2
from webull.trade.trade.v3.order_opration_v3 import OrderOperationV3


class TradeClient:
    def __init__(self, api_client):
        self._init_logger(api_client)
        ClientInitializer.initializer(api_client)
        self.account = Account(api_client)
        self.account_v2 = AccountV2(api_client)
        self.order = OrderOperation(api_client)
        self.order_v2 = OrderOperationV2(api_client)
        self.order_v3 = OrderOperationV3(api_client)
        self.trade_instrument = TradeInstrument(api_client)
        self.trade_calendar = TradeCalendar(api_client)

    def _init_logger(self, api_client):
        # No logger configured, using default console and local file logging.
        if not getattr(api_client, '_stream_logger_set', False) and not getattr(api_client, '_file_logger_set', False):
            log_format = '%(thread)d %(asctime)s %(name)s %(levelname)s %(message)s'
            log_file_path = 'webull_trade_sdk.log'
            api_client.set_stream_logger(stream=sys.stdout, format_string=log_format)
            api_client.set_file_logger(path=log_file_path, log_level=logging.INFO, format_string=log_format)