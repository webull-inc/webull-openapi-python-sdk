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
from datetime import datetime


class BasicResult:
    def __init__(self, pb_basic):
        self.symbol = pb_basic.symbol
        self.instrument_id = pb_basic.instrument_id
        self.timestamp = int(pb_basic.timestamp)
        self.trading_session = pb_basic.trading_session

    def get_symbol(self):
        return self.symbol

    def get_instrument_id(self):
        return self.instrument_id

    def get_timestmap(self):
        return self.timestamp

    def get_timestamp_as_utc(self):
        return datetime.utcfromtimestamp(self.timestamp / 1000.0)

    def get_trading_session(self):
        return self.trading_session

    def __repr__(self):
        return "symbol:%s,instrument_id:%s,timestamp:%d,trading_session:%s" % (self.symbol, self.instrument_id, self.timestamp, self.trading_session)

    def __str__(self):
        return self.__repr__()
