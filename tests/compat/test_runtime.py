"""Offline checks of the SDK's interpreter and native-library boundaries."""

import base64
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager, redirect_stdout
from datetime import datetime
from decimal import Decimal, InvalidOperation
import io
import json
import ssl
import unittest
from unittest.mock import patch

import grpc
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from google.protobuf.message import DecodeError
from requests import Response

import webull.core.headers as headers
from webull.core.auth.algorithm import sha_hmac256
from webull.core.client import ApiClient
from webull.data.data_client import DataClient
from webull.data.data_streaming_client import DataStreamingClient
from webull.data.quotes.subscribe import message_pb2
from webull.data.quotes.subscribe.quote_decoder import QuoteDecoder
from webull.data.quotes.subscribe.snapshot_decoder import SnapshotDecoder
from webull.trade.events import events_pb2, events_pb2_grpc
from webull.trade.trade_client import TradeClient
from webull.trade.trade_events_client import TradeEventsClient


class TestClientCompatibility(unittest.TestCase):
    def test_http_clients_construct_with_token_configuration(self):
        api_client = ApiClient("compat-app", "compat-secret", "us")
        # Constructor checks should not create the SDK's default log files.
        api_client._stream_logger_set = True
        response = Response()
        response.status_code = 200
        response._content = b'{"token_check_enabled": false}'

        with patch.object(
            api_client, "get_response", return_value=response
        ) as get_response:
            data_client = DataClient(api_client)
            trade_client = TradeClient(api_client)

        self.assertIs(data_client.market_data.client, api_client)
        self.assertIs(trade_client.account_v2.client, api_client)
        self.assertEqual(get_response.call_count, 2)
        for call in get_response.call_args_list:
            self.assertEqual(call.args[0].get_action_name(), "/openapi/config")
        self.assertTrue(api_client.default_user_agent()["python-requests"])

    def test_mqtt_client_initializes_with_and_without_tls(self):
        for tls_enable in (False, True):
            with self.subTest(tls_enable=tls_enable):
                client = DataStreamingClient(
                    "compat-app",
                    "compat-secret",
                    "us",
                    "compat-session",
                    http_host="127.0.0.1",
                    mqtt_host="127.0.0.1",
                    tls_enable=tls_enable,
                )
                self.addCleanup(client.disconnect)
                self.assertEqual(client.quotes_session_id, "compat-session")
                self.assertEqual(client.api_client.get_app_key(), "compat-app")
                self.assertIsNone(client.socket())
                if tls_enable:
                    self.assertIsInstance(client._ssl_context, ssl.SSLContext)
                    self.assertEqual(client._ssl_context.verify_mode, ssl.CERT_REQUIRED)
                    self.assertTrue(client._ssl_context.check_hostname)
                else:
                    self.assertIsNone(client._ssl_context)


class TestSigningCompatibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        private_der = cls.private_key.private_bytes(
            serialization.Encoding.DER,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
        cls.secret = base64.b64encode(private_der).decode("ascii")

    def test_rsa_signature_verifies_and_rejects_changed_payload(self):
        payload = "compatibility request \N{EURO SIGN}"
        signature = base64.b64decode(sha_hmac256.get_sign_string(payload, self.secret))
        public_key = self.private_key.public_key()
        public_key.verify(
            signature, payload.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256()
        )
        with self.assertRaises(InvalidSignature):
            public_key.verify(
                signature, b"changed payload", padding.PKCS1v15(), hashes.SHA256()
            )

    def test_rsa_signing_rejects_malformed_private_key(self):
        malformed_secret = base64.b64encode(b"not a DER private key").decode("ascii")
        with self.assertRaises(ValueError):
            sha_hmac256.get_sign_string("compatibility request", malformed_secret)


class TestQuoteDecodingCompatibility(unittest.TestCase):
    def test_snapshot_decodes_price_and_timestamp(self):
        snapshot = message_pb2.Snapshot(
            basic=message_pb2.Basic(symbol="TEST", timestamp="1700000000123"),
            trade_time="1700000000000",
            price="123.45",
            volume="10",
        )
        result = SnapshotDecoder().parse(snapshot.SerializeToString())
        self.assertEqual(result.get_basic().get_symbol(), "TEST")
        self.assertEqual(
            result.get_basic().get_timestamp_as_utc(),
            datetime(2023, 11, 14, 22, 13, 20, 123000),
        )
        self.assertEqual(result.get_last_trade_time(), 1700000000000)
        self.assertEqual(result.get_price(), Decimal("123.45"))
        self.assertEqual(result.get_volume(), Decimal("10"))
        self.assertIsNone(result.get_ext_price())

    def test_quote_decodes_repeated_order_book_entries(self):
        quote = message_pb2.Quote(
            basic=message_pb2.Basic(symbol="TEST", timestamp="1700000000123"),
            asks=[message_pb2.AskBid(price="123.46", size="2")],
            bids=[message_pb2.AskBid(price="123.44", size="3")],
        )
        result = QuoteDecoder().parse(quote.SerializeToString())
        self.assertEqual(
            [entry.get_price() for entry in result.get_asks()], [Decimal("123.46")]
        )
        self.assertEqual([entry.get_size() for entry in result.get_bids()], ["3"])

    def test_snapshot_rejects_invalid_wire_and_numeric_payloads(self):
        malformed_price = message_pb2.Snapshot(
            basic=message_pb2.Basic(timestamp="1700000000123"),
            price="invalid",
        ).SerializeToString()
        for payload, exception_type in (
            (b"\x0a\x05x", DecodeError),
            (malformed_price, InvalidOperation),
        ):
            with self.subTest(exception_type=exception_type):
                with self.assertRaises(exception_type):
                    SnapshotDecoder().parse(payload)


class TestGrpcCompatibility(unittest.TestCase):
    @contextmanager
    def _serve(self, servicer):
        with ThreadPoolExecutor(max_workers=1) as executor:
            server = grpc.server(executor)
            events_pb2_grpc.add_EventServiceServicer_to_server(servicer, server)
            port = server.add_insecure_port("127.0.0.1:0")
            self.assertNotEqual(port, 0)
            server.start()
            try:
                yield "127.0.0.1:{}".format(port)
            finally:
                self.assertTrue(
                    server.stop(0).wait(timeout=5), "gRPC server did not stop"
                )

    def test_signed_subscription_stream_dispatches_protobuf_and_json(self):
        requests = []
        metadata = []

        class EventService(events_pb2_grpc.EventServiceServicer):
            def Subscribe(self, request, context):
                requests.append(request)
                metadata.extend(context.invocation_metadata())
                yield events_pb2.SubscribeResponse(
                    eventType=events_pb2.SubscribeSuccess, payload="connected"
                )
                yield events_pb2.SubscribeResponse(eventType=events_pb2.Ping)
                yield events_pb2.SubscribeResponse(
                    eventType=8,
                    subscribeType=7,
                    contentType="application/json",
                    payload='{"status": "filled", "quantity": 2}',
                )

        client = TradeEventsClient("compat-app", "compat-secret", host="127.0.0.1")
        connected = []
        messages = []
        client.on_connect = lambda client, payload, response: connected.append(payload)
        client.on_events_message = lambda event, subscription, payload, response: (
            messages.append((event, subscription, payload))
        )
        with redirect_stdout(io.StringIO()):
            request, sign_metadata = client._build_request(
                "compat-app", "compat-secret", ["compat-account"]
            )
        with self._serve(EventService()) as target:
            with grpc.insecure_channel(target) as channel:
                stub = events_pb2_grpc.EventServiceStub(channel)
                for response in stub.Subscribe(
                    request, metadata=sign_metadata, timeout=5
                ):
                    client._easy_handler(response)

        self.assertEqual(list(requests[0].accounts), ["compat-account"])
        self.assertEqual(dict(metadata)[headers.APP_KEY], "compat-app")
        self.assertTrue(dict(metadata)[headers.SIGNATURE])
        self.assertEqual(connected, ["connected"])
        self.assertEqual(messages, [(8, 7, {"status": "filled", "quantity": 2})])

    def test_event_handler_rejects_malformed_json_before_callback(self):
        client = TradeEventsClient("compat-app", "compat-secret", host="127.0.0.1")
        messages = []
        client.on_events_message = lambda *args: messages.append(args)
        response = events_pb2.SubscribeResponse(
            eventType=8, contentType="application/json", payload="{invalid"
        )
        with self.assertRaises(json.JSONDecodeError):
            client._easy_handler(response)
        self.assertEqual(messages, [])

    def test_subscription_surfaces_grpc_error_status(self):
        class RejectedService(events_pb2_grpc.EventServiceServicer):
            def Subscribe(self, request, context):
                context.abort(
                    grpc.StatusCode.PERMISSION_DENIED, "compatibility rejection"
                )

        with self._serve(RejectedService()) as target:
            with grpc.insecure_channel(target) as channel:
                stub = events_pb2_grpc.EventServiceStub(channel)
                with self.assertRaises(grpc.RpcError) as raised:
                    list(stub.Subscribe(events_pb2.SubscribeRequest(), timeout=5))
        self.assertEqual(raised.exception.code(), grpc.StatusCode.PERMISSION_DENIED)
        self.assertEqual(raised.exception.details(), "compatibility rejection")


if __name__ == "__main__":
    unittest.main()
