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
from webull.core.request import ApiRequest

class BatchHistoricalBarsRequest(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/openapi/market-data/stock/batch-bars", version='v2', method="POST", body_params={})

    def set_symbols(self, symbol):
        self.add_body_params("symbols", symbol)

    def set_category(self, category):
        self.add_body_params("category", category)

    def set_timespan(self, timespan):
        self.add_body_params("timespan", timespan)

    def set_count(self, count='200'):
        self.add_body_params("count", count)

    def set_real_time_required(self, real_time_required):
        if real_time_required:
            self.add_body_params("real_time_required", real_time_required)

    def set_trading_sessions(self, trading_sessions):
        if trading_sessions:
            if isinstance(trading_sessions, list):
                self.add_body_params("trading_sessions", ','.join(trading_sessions))
            else:
                self.add_body_params("trading_sessions", trading_sessions)

    def set_start_time(self, start_time):
        """
        Set the start time for querying bars.

        :param start_time: Timestamp in milliseconds (Long).
        """
        if start_time is not None:
            self.add_body_params("start_time", start_time)

    def set_end_time(self, end_time):
        """
        Set the end time for querying bars. Delayed permission will auto-offset time.

        :param end_time: Timestamp in milliseconds (Long).
        """
        if end_time is not None:
            self.add_body_params("end_time", end_time)
