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


class EventSnapshotResult:
    def __init__(self, pb_event_snapshot):
        self.basic = BasicResult(pb_event_snapshot.basic)
        self.price = Decimal(pb_event_snapshot.price) if pb_event_snapshot.price else None
        self.volume = Decimal(pb_event_snapshot.volume) if pb_event_snapshot.volume else None
        self.last_trade_time = int(pb_event_snapshot.last_trade_time) if pb_event_snapshot.last_trade_time else None
        self.open_interest = Decimal(pb_event_snapshot.open_interest) if pb_event_snapshot.open_interest else None
        self.yes_ask = Decimal(pb_event_snapshot.yes_ask) if pb_event_snapshot.yes_ask else None
        self.yes_ask_size = Decimal(pb_event_snapshot.yes_ask_size) if pb_event_snapshot.yes_ask_size else None
        self.yes_bid = Decimal(pb_event_snapshot.yes_bid) if pb_event_snapshot.yes_bid else None
        self.yes_bid_size = Decimal(pb_event_snapshot.yes_bid_size) if pb_event_snapshot.yes_bid_size else None
        self.no_bid = Decimal(pb_event_snapshot.no_bid) if pb_event_snapshot.no_bid else None
        self.no_bid_size = Decimal(pb_event_snapshot.no_bid_size) if pb_event_snapshot.no_bid_size else None
        self.no_ask = Decimal(pb_event_snapshot.no_ask) if pb_event_snapshot.no_ask else None
        self.no_ask_size = Decimal(pb_event_snapshot.no_ask_size) if pb_event_snapshot.no_ask_size else None

    def get_basic(self):
        return self.basic

    def get_price(self):
        return self.price

    def get_volume(self):
        return self.volume

    def get_last_trade_time(self):
        return self.last_trade_time

    def get_open_interest(self):
        return self.open_interest

    def get_yes_bid(self):
        return self.yes_bid

    def get_yes_bid_size(self):
        return self.yes_bid_size

    def get_yes_ask(self):
        return self.yes_ask

    def get_yes_ask_size(self):
        return self.yes_ask_size

    def get_no_bid(self):
        return self.no_bid

    def get_no_bid_size(self):
        return self.no_bid_size

    def get_no_ask(self):
        return self.no_ask

    def get_no_ask_size(self):
        return self.no_ask_size

    def __repr__(self):
        attrs = ['price', 'volume', 'last_trade_time', 'open_interest']
        yes_attrs = [f"yes_{name}" for name in ['bid', 'bid_size', 'ask', 'ask_size']]
        no_attrs = [f"no_{name}" for name in ['bid', 'bid_size', 'ask', 'ask_size']]
        all_attrs = attrs + yes_attrs + no_attrs
        attr_str = ', '.join(f"{name}:{getattr(self, name)}" for name in all_attrs)
        return f"{self.basic}, {attr_str}"

    def __str__(self):
        return self.__repr__()
