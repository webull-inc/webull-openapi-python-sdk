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

from webull.data.request.subscribe_request import SubscribeRequest
from webull.data.request.unsubscribe_request import UnsubcribeRequest


class MarketDataStreaming:
    def __init__(self, api_client):
        self.client = api_client

    def subscribe(self, session_id, symbols, category, sub_types, depth=None, overnight_required=None):
        """
       Real-time quotes unsubscribe interface is subscribed to real-time quotes pushes according to symbol and data type.

       :param session_id: Create the sessionId used for the connection
       :param symbols: Such as: [AAPL,TSLA]
       :param category: Security type, enumeration
       :param sub_types: Unsubscribe data type, such as: [SNAPSHOT]、SubType Required when unsubscribe_all is empty
        or not true
       :param depth: Level 2 subscription levels.
        10 levels by default, up to 50 levels for U.S. stocks.
       :param overnight_required: Whether to include the night session, the default is not included
       """
        request = SubscribeRequest()
        request.set_session_id(session_id)
        request.set_symbols(symbols)
        request.set_category(category)
        request.set_sub_types(sub_types)
        request.set_depth(depth)
        request.set_overnight_required(overnight_required)
        response = self.client.get_response(request)
        return response

    def unsubscribe(self, session_id, symbols=None, category=None, sub_types=None, unsubscribe_all=False):
        """
        Real-time quotes unsubscribe interface is subscribed to real-time quotes pushes according to symbol and data type.
        When unsubscribing from the interface, you get no result returned if it succeeds, and Error is returned if it fails.

        :param session_id: Create the sessionId used for the connection
        :param symbols: Such as: [AAPL,TSLA]
        :param category: Security type, enumeration
        :param sub_types: Unsubscribe data type, such as: [SNAPSHOT]、SubType Required when unsubscribe_all is empty
         or not true
        :param unsubscribe_all: boolean false (true means canceling all real-time market subscriptions.
         When unsubscribe_all is true, symbols, category, sub_types can be empty)
        """
        request = UnsubcribeRequest()
        request.set_session_id(session_id)
        request.set_symbols(symbols)
        request.set_category(category)
        request.set_sub_types(sub_types)
        request.set_unsubscribe_all(unsubscribe_all)
        response = self.client.get_response(request)
        return response
