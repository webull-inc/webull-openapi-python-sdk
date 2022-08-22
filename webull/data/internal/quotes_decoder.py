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

from webull.data.internal.quotes_payload_decoder import Utf8Decoder

class QuotesDecoder:
    def __init__(self):
        self._payload_decoders = {}
        self._default_decoder = Utf8Decoder()

    def register_payload_decoder(self, payload_type, decoder):
        self._payload_decoders[payload_type] = decoder

    def decode(self, message):
        quotes_topic = message.topic
        if quotes_topic:
            payload = message.payload
            decoded_payload = self.decode_payload(quotes_topic, payload)
            return (quotes_topic, decoded_payload)
        return None

    def decode_payload(self, quotes_topic, payload):
        decoder = self._payload_decoders.get(quotes_topic)
        if decoder:
            return decoder.parse(payload)
        else:
            return self._default_decoder.parse(payload)
