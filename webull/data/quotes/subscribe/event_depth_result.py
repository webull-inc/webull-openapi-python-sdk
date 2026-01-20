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

from webull.data.quotes.subscribe.basic_result import BasicResult
from webull.data.quotes.subscribe.ask_bid_result import AskBidResult


class EventDepthResult:
    def __init__(self, pb_event_depth):
        self.basic = BasicResult(pb_event_depth.basic)
        self.yes_bids = []
        if pb_event_depth.yes_bids:
            for bid in pb_event_depth.yes_bids:
                self.yes_bids.append(AskBidResult(bid))
        self.no_bids = []
        if pb_event_depth.no_bids:
            for bid in pb_event_depth.no_bids:
                self.no_bids.append(AskBidResult(bid))

    def get_basic(self):
        return self.basic

    def get_yes_bids(self):
        return self.yes_bids

    def get_no_bids(self):
        return self.no_bids

    def __repr__(self):
        return "basic: %s,yes_bids:%s,no_bids:%s" % (self.basic, self.yes_bids, self.no_bids)

    def __str__(self):
        return self.__repr__()
