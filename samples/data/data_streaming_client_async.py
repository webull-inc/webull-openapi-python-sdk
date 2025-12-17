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

import time
import uuid

from webull.data.common.category import Category
from webull.data.common.subscribe_type import SubscribeType
from webull.data.data_streaming_client import DataStreamingClient


your_app_key = "</your_app_key>"
your_app_secret = "</your_app_secret>"
optional_api_endpoint = "</optional_quotes_endpoint>"
optional_quotes_endpoint = "</optional_quotes_endpoint>"
region_id = '<region_id>'
# The token_dir parameter can be used to specify the directory for storing the 2FA token. Both absolute and relative paths are supported and this option has the highest priority.
# Alternatively, the storage directory can be configured via an environment variable with the key WEBULL_OPENAPI_TOKEN_DIR, which also supports both absolute and relative paths.
# If neither is specified, the default configuration will be used, and the token will be stored at conf/token.txt under the current working directory.
# token_dir = "<your_token_dir>"
# data_streaming_client.set_token_dir(token_dir)

session_id = uuid.uuid4().hex
data_streaming_client = DataStreamingClient(your_app_key, your_app_secret, region_id, session_id,
                                    http_host=optional_api_endpoint,
                                    mqtt_host=optional_quotes_endpoint)

if __name__ == '__main__':
    def my_connect_success_func(client, api_client, quotes_session_id):
        print("connect success with session_id:%s" % quotes_session_id)
        # subscribe
        symbols = ['00700']
        sub_types = [SubscribeType.QUOTE.name, SubscribeType.SNAPSHOT.name, SubscribeType.TICK.name]
        client.subscribe(symbols, Category.HK_STOCK.name, sub_types)


    def my_quotes_message_func(client, topic, quotes):
        print("receive message: topic:%s, quotes:%s" % (topic, quotes))


    def my_subscribe_success_func(client, api_client, quotes_session_id):
        print("subscribe success with session_id:%s" % quotes_session_id)


    # set connect success callback func
    data_streaming_client.on_connect_success = my_connect_success_func
    # set quotes receiving callback func
    data_streaming_client.on_quotes_message = my_quotes_message_func
    # set subscribe success callback func
    data_streaming_client.on_subscribe_success = my_subscribe_success_func

    # the async mode, processing in another thread
    data_streaming_client.connect_and_loop_start()

    ticker = 60
    print("will remove subscription after %s seconds..." % ticker)
    time.sleep(ticker)

    subscribe_success = data_streaming_client.get_subscribe_success()
    quotes_session_id = data_streaming_client.get_session_id()
    if subscribe_success:
        print("start remove subscription...")
        data_streaming_client.unsubscribe(unsubscribe_all=True)
        print("remove subscription finish")
    else:
        print("Do not remove subscription, subscribe_success:%s", subscribe_success)

    start_time = time.time()
    wait_time = 1
    while True:
        elapsed = int(time.time() - start_time)
        if elapsed >= ticker:
            print("Wait completed, start subscribing...")
            break
        print("Waiting {} seconds before subscription... (elapsed {}s / {}s)".format(wait_time, elapsed, ticker))
        time.sleep(wait_time)

    # subscribe
    connect_success = data_streaming_client.get_connect_success()
    if connect_success:
        symbols = ['00700']
        sub_types = [SubscribeType.QUOTE.name, SubscribeType.SNAPSHOT.name, SubscribeType.TICK.name]
        data_streaming_client.subscribe(symbols, Category.HK_STOCK.name, sub_types)
        print("add subscription...")
    else:
        print("Do not add subscription, connect_success:%s", connect_success)

    print("will stop processing after %s seconds" % ticker)
    time.sleep(ticker)
    data_streaming_client.loop_stop()
    print("processing done")


