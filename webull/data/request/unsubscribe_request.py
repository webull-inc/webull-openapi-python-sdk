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


class UnsubcribeRequest(ApiRequest):
    def __init__(self):
        ApiRequest.__init__(self, "/market-data/streaming/unsubscribe", version='v2', method="POST", query_params={})
        self.set_body_params({})

    def set_session_id(self, session_id):
        self.add_body_params("session_id", session_id)

    def set_symbols(self, symbols):
        if symbols:
            self.add_body_params("symbols", symbols)

    def set_category(self, category):
        if category:
            self.add_body_params("category", category)

    def set_sub_types(self, sub_types):
        if sub_types:
            self.add_body_params("sub_types", sub_types)

    def set_unsubscribe_all(self, unsubscribe_all):
        if unsubscribe_all is not None:
            self.add_body_params("unsubscribe_all", unsubscribe_all)
