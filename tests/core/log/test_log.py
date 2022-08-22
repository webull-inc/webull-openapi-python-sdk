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

import unittest
import sys
from webull.core.client import ApiClient
from webull.core.http.initializer.client_initializer import ClientInitializer
from webull.core.request import ApiRequest

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"
api_client = ApiClient(your_app_key, your_app_secret, region_id)
api_client.add_endpoint(region_id, optional_api_endpoint)
ClientInitializer.initializer(api_client)


class TestLog(unittest.TestCase):

    def test_set_stream_logger(self):
        log_format = '%(thread)d %(asctime)s %(name)s %(levelname)s %(message)s'
        api_client.set_stream_logger(stream=sys.stdout, format_string=log_format)
        request = ApiRequest("/sign", protocol="http")
        request.add_query_param("k1", " zhong国=&")
        request.add_query_param("k2", "v2")
        api_client.get_response(request)

    def test_set_file_logger(self):
        log_format = '%(thread)d %(asctime)s %(name)s %(levelname)s %(message)s'
        log_file_path = '<log_file_path>'
        api_client.set_file_logger(path=log_file_path, format_string=log_format)
        request = ApiRequest("/sign", protocol="http")
        request.add_query_param("k1", " zhong国=&")
        request.add_query_param("k2", "v2")
        api_client.get_response(request)
