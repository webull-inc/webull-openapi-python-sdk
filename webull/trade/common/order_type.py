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
from webull.core.common.easy_enum import EasyEnum


class OrderType(EasyEnum):
    MARKET = (1, "MARKET")
    LIMIT = (2, "LIMIT")
    STOP_LOSS = (3, "STOP LOSS")
    STOP_LOSS_LIMIT = (4, "STOP LOSS LIMIT")
    TRAILING_STOP_LOSS = (5, "TRAILING STOP LOSS")
    ENHANCED_LIMIT = (6, "ENHANCED LIMIT")
    AT_AUCTION = (7, "AT AUCTION")
    AT_AUCTION_LIMIT = (8, "AT AUCTION LIMIT")
    ODD_LOT_LIMIT = (9, "ODD LOT LIMIT")
    MARKET_ON_OPEN = (10, "MARKET ON OPEN")
    MARKET_ON_CLOSE = (11, "MARKET ON CLOSE")
