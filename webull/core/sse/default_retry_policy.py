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
import httpx

from webull.core.retry.backoff_strategy import (
    BackoffStrategy, FixedDelayStrategy, JitteredExponentialBackoffStrategy)
from webull.core.retry.retry_condition import (
    MaxRetryTimesCondition, MergeRetryCondition, RetryCondition)
from webull.core.retry.retry_policy import RetryPolicy
from webull.core.retry.retry_policy_context import RetryPolicyContext


class SseSubscribeRetryPolicyContext(RetryPolicyContext):
    """Retry context of the SSE subscription.

    ``http_status_code`` is None when the failure happened on an already
    established stream (connection reset, read timeout, server closed the
    stream) or before any HTTP response was received.
    """

    def __init__(self, exception, retries_attempted, http_status_code):
        super().__init__(None, exception, retries_attempted, http_status_code)

    def __str__(self):
        return "exception:%s, retries:%s, http_status_code:%s" % (
            self.exception, self.retries_attempted, self.http_status_code)


class RetryOnSseHttpStatusCondition(RetryCondition):
    # 429 is the session mutex rejection, it must be retried with backoff.
    # 5xx are transient server side failures.
    DEFAULT_RETRYABLE_HTTP_STATUS_LIST = [429, 500, 502, 503, 504]
    THROTTLING_HTTP_STATUS_LIST = [429]

    def __init__(self, retryable_http_status_list=None):
        if retryable_http_status_list:
            self.retryable_http_status_list = retryable_http_status_list
        else:
            self.retryable_http_status_list = self.DEFAULT_RETRYABLE_HTTP_STATUS_LIST

    def should_retry(self, retry_policy_context):
        http_status_code = retry_policy_context.http_status_code
        if http_status_code is None:
            exception = retry_policy_context.exception
            # A stream closed by the server (no exception) or a transport level
            # failure: the SSE channel has no resume support so a brand new
            # subscription is the only way to keep receiving events.
            if exception is None or isinstance(exception, httpx.TransportError):
                return RetryCondition.RETRY
            # Any other exception (e.g. raised by a user callback or a payload
            # that cannot be decoded) would happen again after reconnecting,
            # surface it to the caller instead, same as the gRPC channel.
            return RetryCondition.NO_RETRY
        if http_status_code in self.retryable_http_status_list:
            if http_status_code in self.THROTTLING_HTTP_STATUS_LIST:
                return RetryCondition.RETRY | RetryCondition.SHOULD_RETRY_WITH_THROTTLING_BACKOFF
            return RetryCondition.RETRY
        # 400/401/403/404/405 are caused by the request itself, retrying with
        # the same parameters would fail again.
        return RetryCondition.NO_RETRY


class DefaultSseSubscribeRetryCondition(RetryCondition):
    def __init__(self, max_retry_times=-1):
        RetryCondition.__init__(self)
        if max_retry_times < 0:
            _conditions = []
        else:
            _conditions = [MaxRetryTimesCondition(max_retry_times)]
        _conditions.append(RetryOnSseHttpStatusCondition())
        self._condition = MergeRetryCondition(_conditions)

    def should_retry(self, retry_policy_context):
        return self._condition.should_retry(retry_policy_context)


class SseSubscribeBackoffStrategy(BackoffStrategy):
    """Fixed delay for regular reconnects, jittered backoff for 429 rejections."""

    DEFAULT_THROTTLED_BASE_DELAY = 5000
    DEFAULT_THROTTLED_MAX_DELAY = 60000

    def __init__(self, fixed_delay=5000, throttled_base_delay=None, throttled_max_delay=None):
        self._fixed_backoff_strategy = FixedDelayStrategy(fixed_delay)
        self._throttled_backoff_strategy = JitteredExponentialBackoffStrategy(
            throttled_base_delay or self.DEFAULT_THROTTLED_BASE_DELAY,
            throttled_max_delay or self.DEFAULT_THROTTLED_MAX_DELAY)

    def compute_delay_before_next_retry(self, retry_policy_context):
        if retry_policy_context.retryable & RetryCondition.SHOULD_RETRY_WITH_THROTTLING_BACKOFF:
            return self._throttled_backoff_strategy.compute_delay_before_next_retry(
                retry_policy_context)
        return self._fixed_backoff_strategy.compute_delay_before_next_retry(
            retry_policy_context)


class DefaultSseSubscribeRetryPolicy(RetryPolicy):
    def __init__(self, max_retry_times=-1, fixed_delay=5000):
        RetryPolicy.__init__(self, DefaultSseSubscribeRetryCondition(max_retry_times),
                             SseSubscribeBackoffStrategy(fixed_delay))
