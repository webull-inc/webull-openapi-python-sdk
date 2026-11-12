import os
import unittest

import google.protobuf

from webull.data.quotes.subscribe.message_pb2 import Snapshot
from webull.trade.events.events_pb2 import SubscribeRequest


class TestProtobufCompatibility(unittest.TestCase):

    def test_expected_protobuf_major_is_installed(self):
        expected_major = os.environ["EXPECTED_PROTOBUF_MAJOR"]

        self.assertEqual(google.protobuf.__version__.split(".", 1)[0], expected_major)

    def test_generated_messages_round_trip(self):
        messages = (
            Snapshot(price="123.45", volume="10"),
            SubscribeRequest(subscribeType=1, accounts=["account-id"]),
        )

        for message in messages:
            with self.subTest(message=message.DESCRIPTOR.full_name):
                restored = type(message)()
                restored.ParseFromString(message.SerializeToString())
                self.assertEqual(restored, message)
