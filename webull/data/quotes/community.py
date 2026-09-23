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

from webull.data.request.create_comment_request import CreateCommentRequest
from webull.data.request.create_post_request import CreatePostRequest
from webull.data.request.get_post_request import GetPostRequest
from webull.data.request.list_hot_stocks_request import ListHotStocksRequest
from webull.data.request.list_my_posts_request import ListMyPostsRequest
from webull.data.request.list_posts_by_symbol_request import ListPostsBySymbolRequest


class Community:
    """Community API operations."""

    def __init__(self, api_client):
        self.client = api_client

    def create_post(self, text, symbol=None, category=None):
        """
        Create a plain-text community post.

        :param text: Post content.
        :param symbol: Optional ticker symbol. Provide it with category.
        :param category: Optional ticker market category. Provide it with symbol.
        :return: Response containing the created post identifier.
        """
        request = CreatePostRequest()
        request.set_text(text)
        request.set_symbol(symbol)
        request.set_category(category)
        return self.client.get_response(request)

    def create_comment(self, post_id, text):
        """
        Create a plain-text comment on an existing community post.

        :param post_id: Parent post identifier.
        :param text: Comment content.
        :return: Response containing the created comment identifier.
        """
        request = CreateCommentRequest()
        request.set_post_id(post_id)
        request.set_text(text)
        return self.client.get_response(request)

    def list_hot_stocks(self):
        """
        List stocks ranked by community activity.

        :return: Response containing hot stock ranking entries.
        """
        request = ListHotStocksRequest()
        return self.client.get_response(request)

    def list_posts_by_symbol(self, symbol, category, keyword=None, pagination_key=None):
        """
        List community posts associated with a symbol.

        :param symbol: Stock symbol.
        :param category: Market category.
        :param keyword: Optional search keyword.
        :param pagination_key: Optional key from the previous response.
        :return: Paginated post list response.
        """
        request = ListPostsBySymbolRequest()
        request.set_symbol(symbol)
        request.set_category(category)
        request.set_keyword(keyword)
        request.set_pagination_key(pagination_key)
        return self.client.get_response(request)

    def get_post(self, post_id):
        """
        Get detailed information for a community post.

        :param post_id: Post identifier.
        :return: Post detail response.
        """
        request = GetPostRequest()
        request.set_post_id(post_id)
        return self.client.get_response(request)

    def list_my_posts(self, pagination_key=None):
        """
        List posts created by the current user.

        :param pagination_key: Optional key from the previous response.
        :return: Paginated post list response.
        """
        request = ListMyPostsRequest()
        request.set_pagination_key(pagination_key)
        return self.client.get_response(request)
