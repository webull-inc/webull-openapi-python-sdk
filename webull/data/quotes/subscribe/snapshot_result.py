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


class SnapshotResult:
    def __init__(self, pb_snapshot):
        self.basic = BasicResult(pb_snapshot.basic)
        self.last_trade_time = int(pb_snapshot.trade_time) if pb_snapshot.trade_time else None
        self.price = Decimal(pb_snapshot.price) if pb_snapshot.price else None
        self.open = Decimal(pb_snapshot.open) if pb_snapshot.open else None
        self.high = Decimal(pb_snapshot.high) if pb_snapshot.high else None
        self.low = Decimal(pb_snapshot.low) if pb_snapshot.low else None
        self.pre_close = Decimal(pb_snapshot.pre_close) if pb_snapshot.pre_close else None
        self.close = Decimal(pb_snapshot.open) if pb_snapshot.open else None
        self.volume = Decimal(pb_snapshot.volume) if pb_snapshot.volume else None
        self.change = Decimal(pb_snapshot.change) if pb_snapshot.change else None
        self.change_ratio = Decimal(pb_snapshot.change_ratio) if pb_snapshot.change_ratio else None
        self.ext_trade_time = int(pb_snapshot.ext_trade_time) if pb_snapshot.ext_trade_time else None
        self.ext_price = Decimal(pb_snapshot.ext_price) if pb_snapshot.ext_price else None
        self.ext_high = Decimal(pb_snapshot.ext_high) if pb_snapshot.ext_high else None
        self.ext_low = Decimal(pb_snapshot.ext_low) if pb_snapshot.ext_low else None
        self.ext_volume = Decimal(pb_snapshot.ext_volume) if pb_snapshot.ext_volume else None
        self.ext_change = Decimal(pb_snapshot.ext_change) if pb_snapshot.ext_change else None
        self.ext_change_ratio = Decimal(pb_snapshot.ext_change_ratio) if pb_snapshot.ext_change_ratio else None
        self.ovn_trade_time = int(pb_snapshot.ovn_trade_time) if pb_snapshot.ovn_trade_time else None
        self.ovn_price = Decimal(pb_snapshot.ovn_price) if pb_snapshot.ovn_price else None
        self.ovn_high = Decimal(pb_snapshot.ovn_high) if pb_snapshot.ovn_high else None
        self.ovn_low = Decimal(pb_snapshot.ovn_low) if pb_snapshot.ovn_low else None
        self.ovn_volume = Decimal(pb_snapshot.ovn_volume) if pb_snapshot.ovn_volume else None
        self.ovn_change = Decimal(pb_snapshot.ovn_change) if pb_snapshot.ovn_change else None
        self.ovn_change_ratio = Decimal(pb_snapshot.ovn_change_ratio) if pb_snapshot.ovn_change_ratio else None

    def get_basic(self):
        return self.basic

    def get_last_trade_time(self):
        return self.last_trade_time

    def get_price(self):
        return self.price

    def get_open(self):
        return self.open

    def get_high(self):
        return self.high

    def get_low(self):
        return self.low

    def get_pre_close(self):
        return self.pre_close

    def get_close(self):
        return self.close

    def get_volume(self):
        return self.volume

    def get_change(self):
        return self.change

    def get_change_ratio(self):
        return self.change_ratio

    def get_ext_trade_time(self):
        return self.ext_trade_time

    def get_ext_price(self):
        return self.ext_price

    def get_ext_high(self):
        return self.ext_high

    def get_ext_low(self):
        return self.ext_low

    def get_ext_volume(self):
        return self.ext_volume

    def get_ext_change(self):
        return self.ext_change

    def get_ext_change_ratio(self):
        return self.ext_change_ratio

    def get_ovn_trade_time(self):
        return self.ovn_trade_time

    def get_ovn_price(self):
        return self.ovn_price

    def get_ovn_high(self):
        return self.ovn_high

    def get_ovn_low(self):
        return self.ovn_low

    def get_ovn_volume(self):
        return self.ovn_volume

    def get_ovn_change(self):
        return self.ovn_change

    def get_ovn_change_ratio(self):
        return self.ovn_change_ratio

    def __repr__(self):
        attrs = ['last_trade_time', 'price', 'open', 'high', 'low', 'pre_close', 'close', 'volume', 'change', 'change_ratio']
        ext_attrs = [f"ext_{name}" for name in ['trade_time', 'price', 'high', 'low', 'volume', 'change', 'change_ratio']]
        ovn_attrs = [f"ovn_{name}" for name in ['trade_time', 'price', 'high', 'low', 'volume', 'change', 'change_ratio']]
        all_attrs = attrs + ext_attrs + ovn_attrs
        attr_str = ', '.join(f"{name}:{getattr(self, name)}" for name in all_attrs)
        return f"{self.basic}, {attr_str}"

    def __str__(self):
        return self.__repr__()
