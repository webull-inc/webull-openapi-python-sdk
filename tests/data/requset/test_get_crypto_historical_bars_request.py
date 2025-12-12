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
from webull.data.common.category import Category
from webull.data.common.timespan import Timespan
from webull.data.request.get_crypto_historical_bars_request import GetCryptoHistoricalBarsRequest

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"
api_client = ApiClient(your_app_key, your_app_secret, region_id)
api_client.add_endpoint(region_id, optional_api_endpoint)
ClientInitializer.initializer(api_client)


class TestGetCryptoHistoricalBarsRequest(unittest.TestCase):

    def test_request(self):
        request = GetCryptoHistoricalBarsRequest()
        request.set_category(Category.US_CRYPTO.name)
        request.set_symbol("BTCUSD")
        request.set_timespan(Timespan.D.name)
        ClientInitializer.initializer(api_client)
        response = api_client.get_response(request)
        self.assertTrue(response.status_code == 200)
