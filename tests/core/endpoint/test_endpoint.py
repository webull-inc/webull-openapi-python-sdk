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
from webull.core.common import api_type
from webull.core.endpoint.default_endpoint_resolver import DefaultEndpointResolver
from webull.core.endpoint.resolver_endpoint_request import ResolveEndpointRequest
from webull.core.http.initializer.client_initializer import ClientInitializer
from webull.data.request.get_instruments_request import GetInstrumentsRequest

optional_api_endpoint = "<api_endpoint>"
your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
region_id = "<region_id>"


class TestEndpoint(unittest.TestCase):

    def test_endpoint(self):
        """
            Set through ApiClient and take effect globally. The sample code is as follows.
        """
        api_client = ApiClient(your_app_key, your_app_secret, region_id)
        api_client.add_endpoint(region_id, optional_api_endpoint)
        ClientInitializer.initializer(api_client)
        request = GetInstrumentsRequest()
        request.set_category("HK_STOCK")
        request.set_symbols("00700")
        api_client.get_response(request)

    def test_quotes_endpoint(self):
        """
            Set by Request, and it only takes effect for the current Request. The sample code is as follows.
        """
        resolver = DefaultEndpointResolver(self)
        _region_id = 'us'
        endpoint_request = ResolveEndpointRequest(_region_id, api_type.QUOTES)
        endpoint = resolver.resolve(endpoint_request)
        self.assertEqual(endpoint, 'usquotes-api.webullfintech.com')

        _region_id = 'hk'
        endpoint_request = ResolveEndpointRequest(_region_id, api_type.QUOTES)
        endpoint = resolver.resolve(endpoint_request)
        self.assertEqual(endpoint, 'quotes-api.webull.hk')

        _region_id = 'jp'
        endpoint_request = ResolveEndpointRequest(_region_id, api_type.QUOTES)
        endpoint = resolver.resolve(endpoint_request)
        self.assertEqual(endpoint, '')

    def test_api_endpoint(self):
        """
            Set by Request, and it only takes effect for the current Request. The sample code is as follows.
        """
        resolver = DefaultEndpointResolver(self)
        _region_id = 'us'
        endpoint_request = ResolveEndpointRequest(_region_id)
        endpoint = resolver.resolve(endpoint_request)
        self.assertEqual(endpoint, 'api.webull.com')

        _region_id = 'hk'
        endpoint_request = ResolveEndpointRequest(_region_id)
        endpoint = resolver.resolve(endpoint_request)
        self.assertEqual(endpoint, 'api.webull.hk')

        _region_id = 'jp'
        endpoint_request = ResolveEndpointRequest(_region_id)
        endpoint = resolver.resolve(endpoint_request)
        self.assertEqual(endpoint, 'api.webull.co.jp')

    def test_event_endpoint(self):
        resolver = DefaultEndpointResolver(self)
        _region_id = 'us'
        endpoint_request = ResolveEndpointRequest(_region_id, api_type.EVENTS)
        endpoint = resolver.resolve(endpoint_request)
        self.assertEqual(endpoint, 'events-api.webull.com')

        _region_id = 'hk'
        endpoint_request = ResolveEndpointRequest(_region_id, api_type.EVENTS)
        endpoint = resolver.resolve(endpoint_request)
        self.assertEqual(endpoint, 'events-api.webull.hk')

        _region_id = 'jp'
        endpoint_request = ResolveEndpointRequest(_region_id, api_type.EVENTS)
        endpoint = resolver.resolve(endpoint_request)
        self.assertEqual(endpoint, 'events-api.webull.co.jp')
