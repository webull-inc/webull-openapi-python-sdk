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


class Get52WHLRequestV2(ApiRequest):
    """
    Request class for 52 Week High/Low Rank API.

    The ranking is not paginated and returns the top 200 results.
    """

    def __init__(self):
        ApiRequest.__init__(self, "/market-data/screeners/week52-high-low/list", version='v3', method="GET",
                            query_params={})

    def set_rank_type(self, rank_type):
        if rank_type:
            self.add_query_param("rank_type", rank_type)

    def set_category(self, category):
        if category:
            self.add_query_param("category", category)

    def set_sort_by(self, sort_by):
        if sort_by:
            self.add_query_param("sort_by", sort_by)

    def set_direction(self, direction):
        if direction:
            self.add_query_param("direction", direction)
