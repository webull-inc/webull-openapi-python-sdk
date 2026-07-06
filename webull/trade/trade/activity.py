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

from webull.trade.request.get_activities_request import GetActivitiesRequest


class Activity:
    def __init__(self, api_client):
        self.client = api_client

    def get_activities(self, account_id, activity_types=None, start_time=None, end_time=None,
                       last_activity_id=None, page_size=10):
        """
        Query cash activities by type with pagination support.
        This interface is currently supported only for Webull US.

        :param account_id: Account ID
        :param activity_types: Activity types filter, comma-separated string (optional)
        :param start_time: Start time filter (optional)
        :param end_time: End time filter (optional)
        :param last_activity_id: The last activity ID of the previous page for cursor-based pagination (optional)
        :param page_size: Number of entries per page, default value is 10
        """
        get_activities_request = GetActivitiesRequest()
        get_activities_request.set_account_id(account_id)
        if activity_types is not None:
            get_activities_request.set_activity_types(activity_types)
        if start_time is not None:
            get_activities_request.set_start_time(start_time)
        if end_time is not None:
            get_activities_request.set_end_time(end_time)
        if last_activity_id is not None:
            get_activities_request.set_last_activity_id(last_activity_id)
        get_activities_request.set_page_size(page_size)
        response = self.client.get_response(get_activities_request)
        return response
