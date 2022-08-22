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

from webull.core.client import ApiClient
from webull.core.http.initializer.client_initializer import ClientInitializer
from webull.data.request.get_instruments_request import GetInstrumentsRequest

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"
# Set the connection timeout to 3 seconds and the read timeout to 6 seconds.
api_client = ApiClient(your_app_key, your_app_secret, region_id,
                           connect_timeout=3,
                           timeout=6)
api_client.add_endpoint(region_id, optional_api_endpoint)
ClientInitializer.initializer(api_client)



class TestTimeout(unittest.TestCase):

    def test_timeout(self):
        request = GetInstrumentsRequest()
        # Set the connection timeout of the request to 2 seconds and the read timeout to 4 seconds, only valid for the current request.
        request.set_connect_timeout(2)
        request.set_read_timeout(4)
        request.set_category("HK_STOCK")
        request.set_symbols("00700")
        api_client.get_response(request)
