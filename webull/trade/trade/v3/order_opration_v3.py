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
from webull.trade.request.v3.preview_order_request import PreviewOrderRequest
from webull.trade.request.v3.place_order_request import PlaceOrderRequest
from webull.trade.request.v3.batch_place_order_request import BatchPlaceOrderRequest
from webull.trade.request.v3.replace_order_request import ReplaceOrderRequest
from webull.trade.request.v3.cancel_order_request import CancelOrderRequest
from webull.trade.request.v3.get_order_detail_request import OrderDetailRequest
from webull.trade.request.v3.get_order_history_request import OrderHistoryRequest
from webull.trade.request.v3.get_order_open_request import OrderOpenRequest
from webull.trade.request.v2.get_order_executions_request import GetOrderExecutionsRequest


class OrderOperationV3:
    def __init__(self, api_client):
        self.client = api_client

    def preview_order(self, account_id, preview_orders, client_combo_order_id=None):
        """
        This interface is currently supported only for Webull HK, Webull US, Webull JP, Webull SG, Webull TH, Webull AU, Webull MY, Webull UK, Webull BR, Webull MX, Webull ZA, Webull EU.
        Support for other regions will be available in future updates.
        """
        preview_order_request = PreviewOrderRequest()
        preview_order_request.set_account_id(account_id=account_id)
        preview_order_request.set_new_orders(new_orders=preview_orders)
        preview_order_request.set_client_combo_order_id(client_combo_order_id=client_combo_order_id)
        response = self.client.get_response(preview_order_request)
        return response

    def place_order(self, account_id, new_orders, client_combo_order_id=None):
        """
        This interface is currently supported only for Webull HK, Webull US, Webull JP, Webull SG, Webull TH, Webull AU, Webull MY, Webull UK, Webull BR, Webull MX, Webull ZA, Webull EU.
        Support for other regions will be available in future updates.
        """
        place_order_request = PlaceOrderRequest()
        place_order_request.set_account_id(account_id=account_id)
        place_order_request.set_new_orders(new_orders=new_orders)
        place_order_request.set_client_combo_order_id(client_combo_order_id=client_combo_order_id)
        place_order_request.add_custom_headers_from_order(new_orders)
        response = self.client.get_response(place_order_request)
        return response

    def batch_place_order(self, account_id, batch_orders):
        """
        This interface is currently supported only for Webull US.
        Support for other regions will be available in future updates.
        """
        batch_place_order_request = BatchPlaceOrderRequest()
        batch_place_order_request.set_account_id(account_id=account_id)
        batch_place_order_request.set_batch_orders(batch_orders=batch_orders)
        batch_place_order_request.add_custom_headers_from_order(batch_orders)
        response = self.client.get_response(batch_place_order_request)
        return response

    def replace_order(self, account_id, modify_orders, client_combo_order_id=None):
        """
        This interface is currently supported only for Webull HK, Webull US, Webull JP, Webull SG, Webull TH, Webull AU, Webull MY, Webull UK, Webull BR, Webull MX, Webull ZA, Webull EU.
        Support for other regions will be available in future updates.
        """
        replace_order_request = ReplaceOrderRequest()
        replace_order_request.set_account_id(account_id=account_id)
        replace_order_request.set_modify_orders(modify_orders=modify_orders)
        replace_order_request.set_client_combo_order_id(client_combo_order_id=client_combo_order_id)
        response = self.client.get_response(replace_order_request)
        return response

    def cancel_order(self, account_id, client_order_id):
        """
        This interface is currently supported only for Webull HK, Webull US, Webull JP, Webull SG, Webull TH, Webull AU, Webull MY, Webull UK, Webull BR, Webull MX, Webull ZA, Webull EU.
        Support for other regions will be available in future updates.
        """
        cancel_order_request = CancelOrderRequest()
        cancel_order_request.set_account_id(account_id=account_id)
        cancel_order_request.set_client_order_id(client_order_id=client_order_id)
        response = self.client.get_response(cancel_order_request)
        return response

    def get_order_detail(self, account_id, client_order_id):
        """
        This interface is currently supported only for Webull HK, Webull US, Webull JP, Webull SG, Webull TH, Webull AU, Webull MY, Webull UK, Webull BR, Webull MX, Webull ZA, Webull EU.
        Support for other regions will be available in future updates.

        Response fields (per order item, US market only):
        - leg_in_or_out: Indicates whether this order is legging in or out. Values: LEG_IN, LEG_OUT.
        - position_id: The unique position identifier of the target leg.
        - leg_in_strategy: The target strategy type after legging in (e.g., VERTICAL, CALENDAR, STRANGLE, STRADDLE, IRON_CONDOR, BUTTERFLY, CUSTOM).
        """
        order_detail_request = OrderDetailRequest()
        order_detail_request.set_account_id(account_id=account_id)
        order_detail_request.set_client_order_id(client_order_id=client_order_id)
        response = self.client.get_response(order_detail_request)
        return response

    def get_order_history(self, account_id, page_size=None, start_date=None, end_date=None, last_client_order_id=None):
        """
        This interface is currently supported only for Webull HK, Webull US, Webull JP, Webull SG, Webull TH, Webull AU, Webull MY, Webull UK, Webull BR, Webull MX, Webull ZA, Webull EU.
        Support for other regions will be available in future updates.

        Historical orders. If they are group orders, will be returned together,
        and the number of orders returned on one-page may exceed the page_size.

        :param account_id: Account ID
        :param page_size: Limit the number of records per query to 10 by default.
        :param start_date: Start date (if empty, the default is the last 7 days), in the format of yyyy-MM-dd.
        :param end_date: End date (if empty, the default is the last 7 days), in the format of yyyy-MM-dd.
        :param last_client_order_id: The last client order ID from the previous response. For the first page query,
        this parameter is not required.

        Response fields (per order item, US market only):
        - leg_in_or_out: Indicates whether this order is legging in or out. Values: LEG_IN, LEG_OUT.
        - position_id: The unique position identifier of the target leg.
        - leg_in_strategy: The target strategy type after legging in (e.g., VERTICAL, CALENDAR, STRANGLE, STRADDLE, IRON_CONDOR, BUTTERFLY, CUSTOM).
        """
        order_history_request = OrderHistoryRequest()
        order_history_request.set_account_id(account_id=account_id)
        if page_size:
            order_history_request.set_page_size(page_size=page_size)
        if start_date:
            order_history_request.set_start_date(start_date=start_date)
        if end_date:
            order_history_request.set_end_date(end_date=end_date)
        if last_client_order_id:
            order_history_request.set_last_client_order_id(last_client_order_id=last_client_order_id)
        response = self.client.get_response(order_history_request)
        return response

    def get_order_open(self, account_id, page_size=None, last_client_order_id=None):
        """
        This interface is currently supported only for Webull HK, Webull US, Webull JP, Webull SG, Webull TH, Webull AU, Webull MY, Webull UK, Webull BR, Webull MX, Webull ZA, Webull EU.
        Support for other regions will be available in future updates.

        Paging query pending orders.

        :param account_id: Account ID
        :param page_size: Limit the number of records per query to 10 by default.
        :param last_client_order_id: The last client order ID from the previous response. For the first page query,
        this parameter is not required.

        Response fields (per order item, US market only):
        - leg_in_or_out: Indicates whether this order is legging in or out. Values: LEG_IN, LEG_OUT.
        - position_id: The unique position identifier of the target leg.
        - leg_in_strategy: The target strategy type after legging in (e.g., VERTICAL, CALENDAR, STRANGLE, STRADDLE, IRON_CONDOR, BUTTERFLY, CUSTOM).
        """
        order_open_request = OrderOpenRequest()
        order_open_request.set_account_id(account_id=account_id)
        if page_size:
            order_open_request.set_page_size(page_size=page_size)
        if last_client_order_id:
            order_open_request.set_last_client_order_id(last_client_order_id=last_client_order_id)
        response = self.client.get_response(order_open_request)
        return response

    def get_order_executions(self, account_id, client_order_id=None, start_date=None, end_date=None, last_execution_id=None, page_size=None):
        """
        This interface is currently supported only for Webull HK.
        Support for other regions will be available in future updates.

        Query order execution records within a specified date range.

        :param account_id: Account ID (required).
        :param client_order_id: The 3rd party order ID.
        :param start_date: Start date in the format of yyyy-MM-dd.
        :param end_date: End date in the format of yyyy-MM-dd.
        :param last_execution_id: The last execution ID from the previous response. For the first page query,
        this parameter is not required.
        :param page_size: Number of records per page, defaults to 10.
        """
        request = GetOrderExecutionsRequest()
        request.set_account_id(account_id)
        if start_date:
            request.set_start_date(start_date)
        if end_date:
            request.set_end_date(end_date)
        if last_execution_id:
            request.set_last_execution_id(last_execution_id)
        if client_order_id:
            request.set_client_order_id(client_order_id)
        if page_size:
            request.set_page_size(page_size)
        response = self.client.get_response(request)
        return response
