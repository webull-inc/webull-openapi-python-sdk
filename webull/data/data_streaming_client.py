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

from webull.data.internal.quotes_client import QuotesClient, LOG_ERR
from webull.data.quotes.market_streaming_data import MarketDataStreaming
from webull.data.quotes.subscribe.event_depth_decoder import EventDepthDecoder
from webull.data.quotes.subscribe.event_snapshot_decoder import EventSnapshotDecoder
from webull.data.quotes.subscribe.payload_type import PAYLOAD_TYPE_QUOTE, PAYLOAD_TYPE_SHAPSHOT, PAYLOAD_TYPE_TICK, \
    PAYLOAD_TYPE_EVENT_SHAPSHOT, PAYLOAD_TYPE_EVENT_DEPTH
from webull.data.quotes.subscribe.quote_decoder import QuoteDecoder
from webull.data.quotes.subscribe.snapshot_decoder import SnapshotDecoder
from webull.data.quotes.subscribe.tick_decoder import TickDecoder


class DataStreamingClient(QuotesClient):
    def __init__(self, app_key, app_secret, region_id, session_id, http_host=None,  mqtt_host=None, mqtt_port=1883, tls_enable=True, transport="tcp",
                 retry_policy=None):
        super().__init__(app_key, app_secret, region_id, session_id,
                         http_host=http_host,
                         mqtt_host=mqtt_host,
                         mqtt_port=mqtt_port,
                         tls_enable=tls_enable,
                         transport=transport, retry_policy=retry_policy)
        self._subscribe_success = None
        self._connect_success = None
        self.on_quotes_subscribe = None
        self._on_subscribe_success = None
        # default decoder
        self.register_payload_decoder(PAYLOAD_TYPE_QUOTE, QuoteDecoder())
        self.register_payload_decoder(PAYLOAD_TYPE_SHAPSHOT, SnapshotDecoder())
        self.register_payload_decoder(PAYLOAD_TYPE_TICK, TickDecoder())
        self.register_payload_decoder(PAYLOAD_TYPE_EVENT_DEPTH, EventDepthDecoder())
        self.register_payload_decoder(PAYLOAD_TYPE_EVENT_SHAPSHOT, EventSnapshotDecoder())

    @property
    def on_connect_success(self):
        return self.on_quotes_subscribe

    @on_connect_success.setter
    def on_connect_success(self, func):
        self._connect_success = True
        with self._callback_mutex:
            self.on_quotes_subscribe = func

    @property
    def on_subscribe_success(self):
        return self._on_subscribe_success

    @on_subscribe_success.setter
    def on_subscribe_success(self, func):
        self._subscribe_success = True
        with self._callback_mutex:
            self._on_subscribe_success = func

    def subscribe(self, symbols, category, sub_types, depth=None, overnight_required=None):
        market_data_streaming = MarketDataStreaming(self.api_client)
        response = market_data_streaming.subscribe(self.quotes_session_id, symbols, category, sub_types, depth, overnight_required)
        if response.status_code == 200:
            _on_subscribe_success = self._on_subscribe_success
            if _on_subscribe_success:
                try:
                    _on_subscribe_success(self, self.api_client, self.quotes_session_id)
                except Exception as e:
                    self._easy_log(LOG_ERR, 'Caught exception in on_subscribe_success: %s', e)
                    raise

    def unsubscribe(self, symbols=None, category=None, sub_types=None, unsubscribe_all=False):
        market_data_streaming = MarketDataStreaming(self.api_client)
        market_data_streaming.unsubscribe(self.quotes_session_id, symbols, category, sub_types, unsubscribe_all)

    def get_connect_success(self):
        return self._connect_success

    def get_subscribe_success(self):
        return self._subscribe_success

    def get_session_id(self):
        return self.quotes_session_id

    def easy_log(self, level, msg, *args):
        self._easy_log(level, msg, *args)