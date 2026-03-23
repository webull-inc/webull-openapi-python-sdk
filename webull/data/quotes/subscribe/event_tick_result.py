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

from decimal import Decimal
from webull.data.quotes.subscribe.basic_result import BasicResult


class EventTickResult:
    def __init__(self, pb_event_tick):
        self.basic = BasicResult(pb_event_tick.basic)
        self.time = pb_event_tick.time
        self.yes_price = Decimal(pb_event_tick.yes_price) if pb_event_tick.yes_price else None
        self.no_price = Decimal(pb_event_tick.no_price) if pb_event_tick.no_price else None
        self.volume = pb_event_tick.volume
        self.side = pb_event_tick.side
        self.trade_id = pb_event_tick.trade_id

    def get_basic(self):
        return self.basic

    def get_time(self):
        return self.time

    def get_yes_price(self):
        return self.yes_price

    def get_no_price(self):
        return self.no_price

    def get_volume(self):
        return self.volume

    def get_side(self):
        return self.side

    def get_trade_id(self):
        return self.trade_id

    def __repr__(self):
        return "basic: %s,time: %s,yes_price: %s,no_price:%s,volume:%s,side:%s,trade_id:%s" % (self.basic, self.time, self.yes_price, self.no_price, self.volume, self.side, self.trade_id)

    def __str__(self):
        return self.__repr__()
