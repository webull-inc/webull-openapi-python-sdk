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

import logging
import unittest
from webull.trade.trade_events_client import TradeEventsClient
from webull.core.retry.retry_policy import NO_RETRY_POLICY, RetryPolicy
from webull.core.retry.retry_condition import MaxRetryTimesCondition
from webull.core.retry.backoff_strategy import FixedDelayStrategy, NoDelayStrategy
from unittest.mock import patch

your_app_key = "<your_app_key>"
your_app_secret = "<your_app_secret>"
account_id = "<your_account_id>"
region_id = "hk"

endpoint = "<event_api_endpoint>"


class TestClient(unittest.TestCase):

    def test_error_appkey(self):
        client = TradeEventsClient(your_app_key, your_app_secret, host=endpoint, retry_policy=NO_RETRY_POLICY)
        client.on_log = self._on_log
        try:
            client.do_subscribe(["<your_account_id>"])
        except:
            pass

    def test_error_appkey_and_retry(self):
        retry_policy = RetryPolicy(MaxRetryTimesCondition(3), FixedDelayStrategy(1000))
        client = TradeEventsClient(your_app_key, your_app_secret, host=endpoint, retry_policy=retry_policy)
        client.on_log = self._on_log
        try:
            client.do_subscribe(["<your_account_id>"])
        except:
            pass

    def test_error_accounts(self):
        client = TradeEventsClient("<your_app_key>", your_app_secret, host=endpoint)
        client.enable_logger()
        try:
            client.do_subscribe(["account_mocked"])
        except:
            pass
        try:
            client.do_subscribe("invalid_account_0,account_1")
        except:
            pass
        try:
            client.do_subscribe([])
        except:
            pass

    @patch("core.utils.common.get_uuid")
    def test_replay_connection(self, mock_get_uuid):
        mock_get_uuid.return_value = "the_same_nonce_value"
        retry_policy = RetryPolicy(MaxRetryTimesCondition(10), NoDelayStrategy())
        client = TradeEventsClient("<your_app_key>", your_app_secret, host=endpoint, retry_policy=retry_policy)
        client.on_log = self._on_log
        try:
            client.do_subscribe(["account_mocked"])
        except:
            pass

    def test_normal(self):
        client = TradeEventsClient("<your_app_key>", "<your_app_secret>", host=endpoint)
        client.on_log = self._on_log
        client.do_subscribe(["<your_account_id>"])

    @staticmethod
    def _on_log(level, log_content):
        print(logging.getLevelName(level), log_content)
