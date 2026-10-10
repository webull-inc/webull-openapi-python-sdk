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

from webull.core.client import ApiClient
from webull.data.common.category import Category
from webull.data.data_client import DataClient

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"

api_client = ApiClient(your_app_key, your_app_secret, region_id)
api_client.add_endpoint(region_id, optional_api_endpoint)


if __name__ == '__main__':
    data_client = DataClient(api_client)

    response = data_client.community.create_post(
        "Hello, this is a test post from OpenAPI!",
        symbol="NVDA",
        category=Category.US_STOCK.name,
    )
    if response.status_code == 200:
        print('create_post:', response.json())

    response = data_client.community.create_comment(
        "995005758239301632",
        "Hello, this is a test comment from OpenAPI!",
    )
    if response.status_code == 200:
        print('create_comment:', response.json())

    response = data_client.community.list_hot_stocks()
    if response.status_code == 200:
        print('list_hot_stocks:', response.json())

    response = data_client.community.list_posts_by_symbol("NVDA", Category.US_STOCK.name)
    if response.status_code == 200:
        print('list_posts_by_symbol:', response.json())

    response = data_client.community.get_post("995005758239301632")
    if response.status_code == 200:
        print('get_post:', response.json())

    response = data_client.community.list_my_posts()
    if response.status_code == 200:
        print('list_my_posts:', response.json())
