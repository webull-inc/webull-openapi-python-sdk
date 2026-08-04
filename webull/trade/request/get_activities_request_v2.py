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


class GetActivitiesRequestV2(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/trading/activities/cash-activities/list", version='v3', method="GET",
                            query_params={})

    def set_account_id(self, account_id):
        self.add_query_param("account_id", account_id)

    def set_activity_types(self, activity_types):
        if activity_types is not None:
            self.add_query_param("activity_types", activity_types)

    def set_start_time(self, start_time):
        if start_time is not None:
            self.add_query_param("start_time", start_time)

    def set_end_time(self, end_time):
        if end_time is not None:
            self.add_query_param("end_time", end_time)

    def set_pagination_key(self, pagination_key):
        if pagination_key:
            self.add_query_param("pagination_key", pagination_key)
