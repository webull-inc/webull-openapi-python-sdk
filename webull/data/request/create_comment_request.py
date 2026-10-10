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


class CreateCommentRequest(ApiRequest):
    """Request for creating a plain-text comment on a community post."""

    def __init__(self):
        ApiRequest.__init__(self, "/market-data/communities/comments/create", version="v3", method="POST",
                            body_params={})

    def set_post_id(self, post_id):
        """Set the parent post identifier."""
        self.add_body_params("post_id", post_id)

    def set_text(self, text):
        """Set the comment text."""
        self.add_body_params("text", text)
