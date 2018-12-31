import pytest
import queue

from discord import Payload
from discord import Gateway


class MockWebsocket(object):
    HELLO = '{"t":null,"s":null,"op":10,"d":{"heartbeat_interval":41250,"_trace":["gateway-prd-main-jptr"]}}'
    DISPATCH = '{"t":"READY","s":1,"op":0,"d":{"v":6,"user_settings":{},"user":{"verified":true,"username":"Charlotte","mfa_enabled":false,"id":"botid","email":null,"discriminator":"4148","bot":true,"avatar":"avatarid"},"session_id":"session_id123","relationships":[],"private_channels":[],"presences":[],"guilds":[{"unavailable":true,"id":"someid"},{"unavailable":true,"id":"someid"}],"_trace":["gateway-prd-main-jptr","discord-sessions-prd-1-3"]}}'

    def __init__(self):
        self.next_payload = self.HELLO
        self.last_sent = None
        self.connected = False
        self.has_sent_hello = False

    @staticmethod
    def WebSocket():
        return MockWebsocket()

    def connect(self, endpoint):
        self.connected = True

    def close(self):
        self.connected = False

    def recv(self):
        assert self.connected, "Attempting to recv payloads before connecting."
        if self.next_payload == self.HELLO:
            self.has_sent_hello = True
        return self.next_payload

    def send(self, packet):
        assert self.connected, "Attempting to send payloads before connecting."
        payload = Payload.from_packet(packet)
        if payload == Payload.IDENTIFY:
            assert self.has_sent_hello, "Trying to identify before receiving HELLO."
            self.next_payload = self.DISPATCH
        self.last_sent = payload


@pytest.fixture()
def gateway():
    message_queue = queue.Queue()
    gw = Gateway("False Token",
                 message_queue,
                 MockWebsocket)
    yield gw


def test_connect_handshake_success(gateway):
    hello_payload = '{"t":null,"s":null,"op":10,"d":{"heartbeat_interval":41250,"_trace":["gateway-prd-main-jptr"]}}'
    dispatch_payload = '{"t":"READY","s":1,"op":0,"d":{"v":6,"user_settings":{},"user":{"verified":true,"username":"Charlotte","mfa_enabled":false,"id":"botid","email":null,"discriminator":"4148","bot":true,"avatar":"avatarid"},"session_id":"session_id123","relationships":[],"private_channels":[],"presences":[],"guilds":[{"unavailable":true,"id":"someid"},{"unavailable":true,"id":"someid"}],"_trace":["gateway-prd-main-jptr","discord-sessions-prd-1-3"]}}'

    def send(ws, packet):
        assert ws.connected, "Attempting to send before connecting to websocket."
        assert ws.has_sent_hello, "Sending payload before having received HELLO."
        payload = Payload.from_packet(packet)
        assert payload == Payload.IDENTIFY
        ws.has_sent_identify = True

    handshake_step = 0
    def recv(ws):
        nonlocal handshake_step
        assert ws.connected, "Attempting to receive before connecting to websocket."
        if handshake_step == 0:
            ws.has_sent_hello = True
            response = hello_payload
        elif handshake_step == 1:
            assert ws.has_sent_identify, "Asking for dispatch before sending identify."
            response = dispatch_payload
        handshake_step += 1
        return response

    def WebSocket():
        ws = MockWebsocket()
        ws.send = send.__get__(ws, MockWebsocket)
        ws.recv = recv.__get__(ws, MockWebsocket)
        return ws

    gateway.wslib.WebSocket = WebSocket

    gateway.connect()

    assert handshake_step == 2


def test_receive_payload(gateway):
    hello_payload = '{"t":"hello1","s":3,"op":10,"d":{"heartbeat_interval":41250,"_trace":["gateway-prd-main-jptr"]}}'

    def recv():
        return hello_payload
    gateway.ws = MockWebsocket()
    gateway.ws.recv = recv

    payload = gateway.receive_payload()
    assert payload == Payload.HELLO
    assert payload.data == {"heartbeat_interval":41250,"_trace":["gateway-prd-main-jptr"]}
    assert payload.seq_number == 3
    assert payload.event_name == "hello1"


def test_send_payload(gateway):
    hello_payload = '{"t":"hello1","s":3,"op":10,"d":{"heartbeat_interval":41250,"_trace":["gateway-prd-main-jptr"]}}'

    def send(packet):
        assert Payload.from_packet(packet) == Payload.from_packet(hello_payload)

    gateway.ws = MockWebsocket()
    gateway.ws.send = send

    payload = Payload.from_packet(hello_payload)
    gateway.send_payload(payload)
