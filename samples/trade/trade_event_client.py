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

import logging

from webull.trade.events.types import ORDER_STATUS_CHANGED, EVENT_TYPE_ORDER, EVENT_TYPE_POSITION, \
    POSITION_STATUS_CHANGED
from webull.trade.trade_events_client import TradeEventsClient

your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
account_id = "<your_account_id>"
region_id = "<region_id>"

optional_api_endpoint = "<event_api_endpoint>"


def _on_log(level, log_content):
    print(logging.getLevelName(level), log_content)

def my_on_events_message(event_type, subscribe_type, payload, raw_message):
    if EVENT_TYPE_ORDER == event_type and ORDER_STATUS_CHANGED == subscribe_type:
        print('----request_id:%s----' % payload['request_id'])
        print(payload)
    if EVENT_TYPE_POSITION == event_type and POSITION_STATUS_CHANGED == subscribe_type:
        print('event payload:%s' % payload)

if __name__ == '__main__':

    # Create EventsClient instance
    trade_events_client = TradeEventsClient(your_app_key, your_app_secret, region_id)
    # [Important] For non production environment, you need to set the domain name of the subscription service through events client. For example, the domain name of the UAT environment is set here
    # [Important] For non production environment, you need to set the domain name of the subscription service through events client. For example, the domain name of the UAT environment is set here
    # [Important] For non production environment, you need to set the domain name of the subscription service through events client. For example, the domain name of the UAT environment is set here
    # trade_events_client = TradeEventsClient(your_app_key, your_app_secret, region_id, host=optional_api_endpoint)
    trade_events_client.on_log = _on_log

    # Set the callback function when the event data is received.
    # The data of order status change is printed here

    trade_events_client.on_events_message = my_on_events_message
    # Set the account ID to be subscribed and initiate the subscription. This method is synchronous
    trade_events_client.do_subscribe([account_id])
