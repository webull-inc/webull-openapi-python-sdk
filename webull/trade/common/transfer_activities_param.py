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

from webull.core.utils import validation


class TransferActivitiesParam:
    """
    Parameter object for :meth:`Activity.list_transfers_activities`.

    :param account_id: Account ID (required).
    :param transfer_method: Transfer method filter, comma-separated (e.g. ACATS,CRYPTO_TRANSFER) (optional).
    :param direction: Direction filter: INCOMING or OUTGOING (optional).
    :param status: Status filter, comma-separated: PENDING, COMPLETED, REJECTED, FAILED, CANCELLED (optional).
    :param acats_transfer_types: ACATS transfer types filter, comma-separated: FULL, PARTIAL, RESIDUAL, RECLAIM, OTHER (optional).
    :param start_time: ISO8601 UTC start time of transfer create time (optional).
    :param end_time: ISO8601 UTC end time of transfer create time (optional).
    :param pagination_key: Pagination key from the previous page response; not returned on the last page (optional).
    """

    def __init__(self, account_id, transfer_method=None, direction=None, status=None,
                 acats_transfer_types=None, start_time=None, end_time=None, pagination_key=None):
        validation.assert_string_not_empty(account_id, "account_id")
        self.account_id = account_id
        self.transfer_method = transfer_method
        self.direction = direction
        self.status = status
        self.acats_transfer_types = acats_transfer_types
        self.start_time = start_time
        self.end_time = end_time
        self.pagination_key = pagination_key
