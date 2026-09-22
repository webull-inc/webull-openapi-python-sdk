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
import json

# Control event type values, kept identical to the gRPC EventType enum.
# Declared locally so that the SSE channel does not depend on protobuf.
SUBSCRIBE_SUCCESS = 0
PING = 1
AUTH_ERROR = 2
NUM_OF_CONN_EXCEED = 3
SUBSCRIBE_EXPIRED = 4

# SSE frame names pushed by the server.
EVENT_SUBSCRIBE_SUCCESS = "subscribeSuccess"
EVENT_PING = "ping"
EVENT_BUSINESS = "event"
EVENT_SUBSCRIBE_EXPIRED = "subscribeExpired"
EVENT_AUTH_ERROR = "authError"
EVENT_NUM_OF_CONN_EXCEED = "numOfConnExceed"

# Control frames are identified by the SSE frame name, not by the eventType
# value in the data (zero value fields such as eventType 0 are omitted).
EVENT_NAME_TO_EVENT_TYPE = {
    EVENT_SUBSCRIBE_SUCCESS: SUBSCRIBE_SUCCESS,
    EVENT_PING: PING,
    EVENT_AUTH_ERROR: AUTH_ERROR,
    EVENT_NUM_OF_CONN_EXCEED: NUM_OF_CONN_EXCEED,
    EVENT_SUBSCRIBE_EXPIRED: SUBSCRIBE_EXPIRED,
}


class SseSubscribeResponse:
    """Decoded SSE frame exposing the same fields as the gRPC SubscribeResponse.

    Field names intentionally match the protobuf message (``eventType``,
    ``subscribeType``, ``contentType``, ``payload``, ``requestId``,
    ``timestamp``) so that callbacks written against the gRPC channel keep
    working without changes.
    """

    def __init__(self, event, data):
        """
        Args:
            event: SSE frame name, e.g. ``subscribeSuccess``, ``ping``, ``event``.
            data: raw ``data:`` payload of the frame, a JSON string.

        Raises:
            ValueError: the frame data is not a JSON object.
        """
        self.event = event
        self.raw_data = data
        fields = json.loads(data) if data else {}
        if not isinstance(fields, dict):
            raise ValueError("unexpected sse data, not a json object: %s" % data)
        if event in EVENT_NAME_TO_EVENT_TYPE:
            self.eventType = EVENT_NAME_TO_EVENT_TYPE[event]
        else:
            self.eventType = fields.get("eventType")
        self.subscribeType = fields.get("subscribeType", 0)
        self.contentType = fields.get("contentType", "")
        self.payload = fields.get("payload", "")
        self.requestId = fields.get("requestId", "")
        self.timestamp = fields.get("timestamp", 0)

    def __str__(self):
        return ("event:%s, eventType:%s, subscribeType:%s, contentType:%s, "
                "requestId:%s, timestamp:%s, payload:%s") % (
            self.event, self.eventType, self.subscribeType, self.contentType,
            self.requestId, self.timestamp, self.payload)

    __repr__ = __str__
