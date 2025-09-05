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

from webull.data.quotes.subscribe.message_pb2 import Quote
from webull.data.quotes.subscribe.quote_result import QuoteResult
from webull.data.internal.quotes_payload_decoder import BaseQuotesPayloadDecoder

class QuoteDecoder(BaseQuotesPayloadDecoder):
    def __init__(self):
        super().__init__()

    def parse(self, payload):
        quote = Quote()
        quote.ParseFromString(payload)
        return QuoteResult(quote)
