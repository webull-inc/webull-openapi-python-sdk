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

from webull.core.common.region import Region
from webull.core.exception import error_code
from webull.core.exception.exceptions import ClientException
from webull.trade.request.get_activities_request import GetActivitiesRequest
from webull.trade.request.get_activities_request_v2 import GetActivitiesRequestV2
from webull.trade.request.v3.get_transfer_activities_request import TransferActivitiesRequest
from webull.trade.request.v3.get_transfer_activities_detail_request import TransferActivitiesDetailRequest
from webull.trade.common.transfer_activities_param import TransferActivitiesParam


class Activity:
    def __init__(self, api_client):
        self.client = api_client

    def _assert_us_region(self, operation):
        region_id = self.client.get_region_id()
        if region_id != Region.US.value:
            raise ClientException(
                error_code.SDK_NOT_SUPPORT,
                "%s is currently supported only for Webull US region, current region is %s." % (
                    operation, region_id))

    def get_activities(self, account_id, activity_types=None, start_time=None, end_time=None,
                       last_activity_id=None, page_size=10):
        """
        .. deprecated::
            Use :meth:`list_activities` instead.

        The x-version header distinguishes the legacy and new pagination protocols for this path.

        Query cash activities by type with pagination support.
        This interface is currently supported only for Webull US.

        :param account_id: Account ID
        :param activity_types: Activity types filter, comma-separated string (optional)
        :param start_time: Start time filter (optional)
        :param end_time: End time filter (optional)
        :param last_activity_id: The last activity ID of the previous page for cursor-based pagination (optional)
        :param page_size: Number of entries per page, default value is 10
        """
        get_activities_request = GetActivitiesRequest()
        get_activities_request.set_account_id(account_id)
        if activity_types is not None:
            get_activities_request.set_activity_types(activity_types)
        if start_time is not None:
            get_activities_request.set_start_time(start_time)
        if end_time is not None:
            get_activities_request.set_end_time(end_time)
        if last_activity_id is not None:
            get_activities_request.set_last_activity_id(last_activity_id)
        get_activities_request.set_page_size(page_size)
        response = self.client.get_response(get_activities_request)
        return response

    def list_activities(self, account_id, activity_types=None, start_time=None, end_time=None,
                        pagination_key=None):
        """
        The x-version header distinguishes the legacy and new pagination protocols for this path.

        Query cash activities by type with pagination support.
        This interface is currently supported only for Webull US.

        :param account_id: Account ID
        :param activity_types: Activity types filter, comma-separated string (optional)
        :param start_time: Start time filter (optional)
        :param end_time: End time filter (optional)
        :param pagination_key: Pagination key from the previous page response; not returned on the last page.
        """
        get_activities_request = GetActivitiesRequestV2()
        get_activities_request.set_account_id(account_id)
        if activity_types is not None:
            get_activities_request.set_activity_types(activity_types)
        if start_time is not None:
            get_activities_request.set_start_time(start_time)
        if end_time is not None:
            get_activities_request.set_end_time(end_time)
        if pagination_key is not None:
            get_activities_request.set_pagination_key(pagination_key)
        response = self.client.get_response(get_activities_request)
        return response

    def list_transfers_activities(self, param):
        """
        Query transfer records with pagination support. Results are ordered by create time descending.
        Routes to ACATS or crypto transfer downstream by account type.
        This interface is currently supported only for Webull US.

        Each record is a summary view containing: account_id, transfer_method, transfer_id, direction,
        status, failure_reason, acats_associated_number, acats_transfer_types, create_time, update_time,
        transfer_settlement_date. Detailed fields (acats_control_number, contra_broker, crypto_transaction_hash,
        crypto_from_address, crypto_to_address, cash, positions) are returned only by get_transfer_activity.

        :param param: A :class:`TransferActivitiesParam` object carrying account_id and optional filters.
        """
        self._assert_us_region("list_transfers_activities")
        if not isinstance(param, TransferActivitiesParam):
            raise ClientException(
                error_code.SDK_INVALID_PARAMETER,
                "param should be a TransferActivitiesParam object.")
        get_transfers_request = TransferActivitiesRequest()
        get_transfers_request.set_account_id(param.account_id)
        if param.transfer_method is not None:
            get_transfers_request.set_transfer_method(param.transfer_method)
        if param.direction is not None:
            get_transfers_request.set_direction(param.direction)
        if param.status is not None:
            get_transfers_request.set_status(param.status)
        if param.acats_transfer_types is not None:
            get_transfers_request.set_acats_transfer_types(param.acats_transfer_types)
        if param.start_time is not None:
            get_transfers_request.set_start_time(param.start_time)
        if param.end_time is not None:
            get_transfers_request.set_end_time(param.end_time)
        if param.pagination_key is not None:
            get_transfers_request.set_pagination_key(param.pagination_key)
        response = self.client.get_response(get_transfers_request)
        return response

    def get_transfer_activity_detail(self, account_id, transfer_id):
        """
        Get a single transfer record by account ID and transfer ID.
        This interface is currently supported only for Webull US.

        Returns the full detail view. In addition to the summary fields from list_transfers_activities,
        it also includes: acats_control_number, contra_broker (broker_name, dtc_number, account_type,
        account_number), crypto_transaction_hash, crypto_from_address, crypto_to_address, cash
        (amount, currency, settlement_date) and positions (asset_type is one of EQUITY, OPTION, FUTURES,
        CRYPTO, EVENT, MUTUAL_FUND, BOND; plus symbol, name, cusip, quantity, fee_quantity, total_quantity,
        transfer_price, settlement_date).

        :param account_id: Account ID
        :param transfer_id: Transfer record ID
        """
        self._assert_us_region("get_transfer_activity_detail")
        get_transfer_request = TransferActivitiesDetailRequest()
        get_transfer_request.set_account_id(account_id)
        get_transfer_request.set_transfer_id(transfer_id)
        response = self.client.get_response(get_transfer_request)
        return response
