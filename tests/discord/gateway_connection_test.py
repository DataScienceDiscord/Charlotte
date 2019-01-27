from discord import GatewayConnection
from discord import Payload
from discord import DisconnectionException


class MockWebsocket(object):

    def __init__(self):
        self.connected = False
        self.closed    = False

    @staticmethod
    def WebSocket():
        return MockWebsocket()

    def connect(self, endpoint):
        self.connected = True
        self.connection_endpoint = endpoint

    def close(self):
        self.closed = True
        self.connected = False


class MockLogger(object):

    def __init__(self):
        pass

    @staticmethod
    def getLogger(name):
        return MockLogger()

    def info(self, content, *args):
        assert "SENSITIVE_INFO" not in content
        for arg in args:
            "SENSITIVE_INFO" not in arg


def test_open_connection_success():
    conn = GatewayConnection(wslib=MockWebsocket)

    conn.open()
    assert conn.ws.connection_endpoint == conn.endpoint


def test_open_connection_already_open():
    conn = GatewayConnection(wslib=MockWebsocket)

    conn.open()
    assert conn.ws.connection_endpoint == conn.endpoint

    try:
        conn.open()
        assert False, "Should have raised a value error as the connection is already open."
    except ValueError:
        pass


def test_close_connection():
    conn = GatewayConnection(wslib=MockWebsocket)
    try:
        conn.close()
    except:
        assert False, "Should not raise an error if connection is not open yet, not a big deal."


    conn = GatewayConnection(wslib=MockWebsocket)
    conn.open()
    assert conn.ws.connection_endpoint == conn.endpoint
    assert not conn.ws.closed

    conn.close()
    assert conn.ws.closed

    try:
        conn.close()
    except:
        assert False, "Should not raise an error if connection is already closed, not a big deal."


def test_context():
    with GatewayConnection(wslib=MockWebsocket) as conn:
        assert conn.connected
    assert not conn.connected


def test_connected_same_as_websocket():
    conn = GatewayConnection(wslib=MockWebsocket)

    conn.open()
    assert conn.ws.connected == True
    assert conn.connected    == True

    conn.close()
    assert conn.ws.closed
    assert conn.ws.connected == False
    assert conn.connected    == False


def test_receive_payload_success():
    conn = GatewayConnection(wslib=MockWebsocket)
    conn.open()

    hello_payload = '{"t":"hello1","s":3,"op":10,"d":{"heartbeat_interval":41250,"_trace":["gateway-prd-main-jptr"]}}'
    def recv():
        return hello_payload
    conn.ws.recv = recv

    payload = conn.receive_payload()
    assert payload == Payload.HELLO
    assert payload.data == {"heartbeat_interval":41250,"_trace":["gateway-prd-main-jptr"]}
    assert payload.seq_number == 3
    assert conn.last_seq == 3
    assert payload.event_name == "hello1"


def test_receive_payload_no_seq_number():
    conn = GatewayConnection(wslib=MockWebsocket)
    conn.open()

    hello_payload = '{"t":"hello1","s":3,"op":10,"d":{"heartbeat_interval":41250,"_trace":["gateway-prd-main-jptr"]}}'
    def recv():
        return hello_payload
    conn.ws.recv = recv
    payload = conn.receive_payload()
    assert conn.last_seq == 3


    hello_payload = '{"t":"hello2","s": null,"op":10,"d":{"heartbeat_interval":41250,"_trace":["gateway-prd-main-jptr"]}}'
    def recv():
        return hello_payload
    conn.ws.recv = recv
    payload = conn.receive_payload()
    assert conn.last_seq == 3


def test_receive_payload_empty_packet():
    conn = GatewayConnection(wslib=MockWebsocket)
    conn.open()

    def recv():
        return ""
    conn.ws.recv = recv

    try:
        payload = conn.receive_payload()
        assert False, "Should have raised a disconnection error on empty packet."
    except DisconnectionException:
        pass


def test_send_payload_success():
    conn = GatewayConnection(wslib=MockWebsocket)
    conn.open()

    hello_payload = '{"t":"hello1","s":3,"op":10,"d":{"heartbeat_interval":41250,"_trace":["gateway-prd-main-jptr"]}}'
    def send(packet):
        assert Payload.from_packet(packet) == Payload.from_packet(hello_payload)
    conn.ws.send = send

    payload = Payload.from_packet(hello_payload)
    conn.send_payload(payload)


def test_send_payload_doesnt_log_token():
    conn = GatewayConnection(wslib=MockWebsocket, logging=MockLogger)
    conn.open()

    identify_payload = '{"op": 2, "d": {"token": "SENSITIVE_INFO", "properties": {"$os": "linux", "$browser": "Charlotte", "$device": "Charlotte"}}, "s": null, "t": null}'
    def send(packet):
        assert Payload.from_packet(packet) == Payload.from_packet(identify_payload)
    conn.ws.send = send

    payload = Payload.from_packet(identify_payload)
    conn.send_payload(payload)

    resume_payload = '{"op": 6, "d": {"token": "SENSITIVE_INFO", "properties": {"$os": "linux", "$browser": "Charlotte", "$device": "Charlotte"}}, "s": null, "t": null}'
    def send(packet):
        assert Payload.from_packet(packet) == Payload.from_packet(resume_payload)
    conn.ws.send = send

    payload = Payload.from_packet(resume_payload)
    conn.send_payload(payload)


