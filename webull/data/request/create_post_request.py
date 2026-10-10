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


class CreatePostRequest(ApiRequest):
    """Request for creating a plain-text community post."""

    def __init__(self):
        ApiRequest.__init__(self, "/market-data/communities/posts/create", version="v3", method="POST",
                            body_params={})

    def set_text(self, text):
        """Set the post text."""
        self.add_body_params("text", text)

    def set_symbol(self, symbol):
        """Set the optional ticker symbol."""
        if symbol is not None:
            self.add_body_params("symbol", symbol)

    def set_category(self, category):
        """Set the optional ticker market category."""
        if category is not None:
            self.add_body_params("category", category)
