import pytest
import queue
import threading
import time

from discord import Payload
from discord import Gateway
from discord import DisconnectionException
from discord import InvalidSessionException


class MockConnection(object):

    def __init__(self, run_type="NORMAL", added_payloads=[]):
        self.last_seq = 0
        self.payload_id = 0
        self.payloads_normal = [
            '{"t":null,"s":null,"op":10,"d":{"heartbeat_interval":50,"_trace":["gateway-prd-main-jptr"]}}',
            '{"t":"READY","s":1,"op":0,"d":{"v":6,"user_settings":{},"user":{"verified":true,"username":"Charlotte","mfa_enabled":false,"id":"botid","email":null,"discriminator":"4148","bot":true,"avatar":"avatarid"},"session_id":"session_id123","relationships":[],"private_channels":[],"presences":[],"guilds":[{"unavailable":true,"id":"someid"},{"unavailable":true,"id":"someid"}],"_trace":["gateway-prd-main-jptr","discord-sessions-prd-1-3"]}}',

        ]
        self.payloads_resume = [
            '{"t":null,"s":null,"op":10,"d":{"heartbeat_interval":50,"_trace":["gateway-prd-main-jptr"]}}',
            '{"t":"MESSAGE_CREATE","s":13,"op":0,"d":{"type":0,"tts":false,"timestamp":"2018-12-14T14:24:37.826000+00:00","pinned":false,"nonce":"523143245568409600","mentions":[],"mention_roles":[],"mention_everyone":false,"member":{"roles":[],"mute":false,"joined_at":"2018-12-14T14:18:16.822000+00:00","deaf":false},"id":"523143281433903104","embeds":[],"edited_timestamp":null,"content":"qesdfzsezfsf","channel_id":"523141683379175426","author":{"username":"Et","id":"181098168266653698","discriminator":"5175","avatar":"7625f24396b5fad487d5b90d36315032"},"attachments":[],"guild_id":"523141683379175424"}}'
        ]

        self.payloads_invalid = [
            '{"t":null,"s":null,"op":10,"d":{"heartbeat_interval":50,"_trace":["gateway-prd-main-jptr"]}}',
            '{"t":null,"s":null,"op":9,"d":false}'
        ]

        if run_type == "NORMAL":
            self.payloads = self.payloads_normal
        elif run_type == "RESUME":
            self.payloads = self.payloads_resume
        elif run_type == "INVALID":
            self.payloads = self.payloads_invalid
        self.payloads += added_payloads
        self.connected = False
        self.payload_sent = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def open(self):
        self.connected = True

    def close(self):
        self.connected = False

    def receive_payload(self):
        assert self.connected, "Attempting to recv payloads before connecting."
        if self.payload_id >= len(self.payloads):
            raise DisconnectionException()
        payload = self.payloads[self.payload_id]
        payload = Payload.from_packet(payload)
        self.payload_id += 1
        return payload

    def send_payload(self, payload):
        self.last_payload_sent = payload
        assert self.connected, "Attempting to send payloads before connecting."



def test_connection_interval():
    message_queue = queue.Queue()
    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    for i in range(1000):
        gw.reconnect_counter = i
        assert Gateway.MIN_RECONNECTION_WAIT <= gw.connection_interval <= Gateway.MAX_RECONNECTION_WAIT


def test_send_heartbeats():
    message_queue = queue.Queue()
    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    connection = MockConnection()
    connection.open()
    gw.running = True
    gw.heartbeat_period = 0.05

    connection.heartbeat_counter = 0
    def send_payload(connection, payload):
        if payload == Payload.HEARTBEAT:
            connection.heartbeat_counter += 1
    connection.send_payload = send_payload.__get__(connection, MockConnection)

    def acknowledger():
        counter = 0
        if gw.last_beat != 0:
            assert False, "Wrong test setup."
        while gw.last_beat == 0:
            time.sleep(0.01)
        while gw.running:
            gw.last_ack = time.time()
            time.sleep(0.01)
            counter += 1
            if counter >= 55:
                gw.running = False
                break

    t = threading.Thread(target=acknowledger)
    t.start()

    gw.send_heartbeats(connection)

    assert 10 <= connection.heartbeat_counter <= 12


def test_send_heartbeats_no_acknowledgement():
    message_queue = queue.Queue()
    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    connection = MockConnection()
    connection.open()
    gw.running = True
    gw.heartbeat_period = 0.05

    connection.heartbeat_counter = 0
    def send_payload(connection, payload):
        if payload == Payload.HEARTBEAT:
            connection.heartbeat_counter += 1
    connection.send_payload = send_payload.__get__(connection, MockConnection)

    gw.send_heartbeats(connection)

    assert connection.heartbeat_counter == 2 # Setup beat -> actual first beat -> close
    assert not connection.connected


def test_process_payload_heartbeat_request():
    message_queue = queue.Queue()
    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    connection = MockConnection()
    connection.open()

    heartbeat_req = '{"t":null,"s":null,"op":1,"d":null}'
    heartbeat_req = Payload.from_packet(heartbeat_req)
    gw.process_payload(heartbeat_req, connection)

    assert connection.last_payload_sent == Payload.HEARTBEAT


def test_process_payload_heartbeat_ack():
    message_queue = queue.Queue()
    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    connection = MockConnection()
    connection.open()

    heartbeat_ack = '{"t":null,"s":null,"op":11,"d":null}'
    heartbeat_ack = Payload.from_packet(heartbeat_ack)
    gw.process_payload(heartbeat_ack, connection)

    epsilon = 0.01
    assert abs(gw.last_ack - time.time()) < epsilon


def test_process_payload_message():
    message_queue = queue.Queue()
    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    connection = MockConnection()
    connection.open()

    message = '{"t":"MESSAGE_CREATE","s":13,"op":0,"d":{"type":0,"tts":false,"timestamp":"2018-12-14T14:24:37.826000+00:00","pinned":false,"nonce":"523143245568409600","mentions":[],"mention_roles":[],"mention_everyone":false,"member":{"roles":[],"mute":false,"joined_at":"2018-12-14T14:18:16.822000+00:00","deaf":false},"id":"523143281433903104","embeds":[],"edited_timestamp":null,"content":"qesdfzsezfsf","channel_id":"523141683379175426","author":{"username":"Et","id":"181098168266653698","discriminator":"5175","avatar":"7625f24396b5fad487d5b90d36315032"},"attachments":[],"guild_id":"523141683379175424"}}'
    message = Payload.from_packet(message)
    gw.process_payload(message, connection)

    added = message_queue.get()
    assert added.content == "qesdfzsezfsf"


def test_process_payloads_handles_disconnection():
    message_queue = queue.Queue()
    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    connection = MockConnection()
    connection.open()

    def receive_payload(connection):
        raise DisconnectionException()
    connection.receive_payload = receive_payload.__get__(connection, MockConnection)

    def ensure_thread_stops():
        time.sleep(0.5)
        gw.running = False

    t = threading.Thread(target=ensure_thread_stops)
    t.start()

    gw.running = True
    loop_start = time.time()
    try:
        gw.process_payloads(connection)
    except:
        assert False, "No exception should have been raised."
    loop_end = time.time()

    epsilon = 0.2
    assert abs(loop_end - loop_start) < epsilon, "Loop should have ended on disconnection."


def test_perform_handshake():
    message_queue = queue.Queue()
    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    connection = MockConnection()
    connection.open()

    connection.heartbeat_counter = 0
    sent = []
    def send_payload(connection, payload):
        sent.append(payload)
    connection.send_payload = send_payload.__get__(connection, MockConnection)


    gw.perform_handshake(connection)

    assert gw.heartbeat_period == 50 / 1000
    assert sent[0] == Payload.IDENTIFY
    assert gw.session_id == "session_id123"


def test_perform_handshake_resume():
    message_queue = queue.Queue()
    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    connection = MockConnection(run_type="RESUME")
    connection.open()

    connection.heartbeat_counter = 0
    sent = []
    def send_payload(connection, payload):
        sent.append(payload)
    connection.send_payload = send_payload.__get__(connection, MockConnection)


    gw.perform_handshake(connection, resume=True)

    assert gw.heartbeat_period == 50 / 1000
    assert sent[0] == Payload.RESUME


def test_perform_handshake_invalid():
    message_queue = queue.Queue()
    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    connection = MockConnection(run_type="INVALID")
    connection.open()

    connection.heartbeat_counter = 0
    sent = []
    def send_payload(connection, payload):
        sent.append(payload)
    connection.send_payload = send_payload.__get__(connection, MockConnection)

    try:
        gw.perform_handshake(connection)
        assert False, "Should have raise an InvalidSessionException."
    except InvalidSessionException:
        pass
    except:
        assert False, "Raised wrong exception."


def test_run():
    message_queue = queue.Queue()
    Gateway.MIN_RECONNECTION_WAIT = 0.05
    Gateway.MAX_RECONNECTION_WAIT = 0.05

    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    def ensure_thread_stops():
        time.sleep(0.5)
        gw.stop()

    t = threading.Thread(target=ensure_thread_stops)
    t.start()

    gw.running = True
    gw.run()


def test_run_reconnection():
    message_queue = queue.Queue()
    Gateway.MIN_RECONNECTION_WAIT = 0.05
    Gateway.MAX_RECONNECTION_WAIT = 0.05

    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)


    connections = []
    resumings = []
    def perform_handshake(gw, connection, resuming):
        connections.append(connection)
        resumings.append(resuming)
        # 1st is normal connection ends after non blocking process_payloads
        # 2nd is reconnection with resume, ends after non blocking process_payloads
        # 3rd is reconnection with failed resume, should lead to 4th
        # 4th should be reconnection without resume
        if len(connections) == 3:
            raise InvalidSessionException()
        if len(connections) >= 4: # Make 4th connection be the last
            raise ValueError()
    gw.perform_handshake = perform_handshake.__get__(gw, Gateway)

    def process_payloads(gw, connection):
        # Normally blocking, exiting indicates a disconnection
        return
    gw.process_payloads = process_payloads.__get__(gw, Gateway)
    gw.heartbeat_period = 0.05
    gw.running = True

    try:
        gw.run()
        assert False, "Should have raised a ValueError on second connection."
    except ValueError:
        pass
    finally:
        gw.stop()

    assert len(connections) == 4
    assert len(set(connections)) == 4, "There should be different connections each run."
    assert resumings[0] == False
    assert resumings[1] == True
    assert resumings[2] == True
    assert resumings[3] == False, "After the failed resume 4th should be normal reconnection."
    assert gw.reconnect_counter == 1


def test_run_invalid_session_resume():
    message_queue = queue.Queue()
    Gateway.MIN_RECONNECTION_WAIT = 0.05
    Gateway.MAX_RECONNECTION_WAIT = 0.05

    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    def perform_handshake(gw, connection, resuming):
        raise InvalidSessionException()
    gw.perform_handshake = perform_handshake.__get__(gw, Gateway)

    def ensure_thread_stops():
        time.sleep(0.5)
        gw.stop()
    t = threading.Thread(target=ensure_thread_stops)
    t.start()

    gw.running = True
    gw.run()


def test_run_disconnection_resume():
    message_queue = queue.Queue()
    Gateway.MIN_RECONNECTION_WAIT = 0.05
    Gateway.MAX_RECONNECTION_WAIT = 0.05

    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    def perform_handshake(gw, connection, resuming):
        raise DisconnectionException()
    gw.perform_handshake = perform_handshake.__get__(gw, Gateway)

    def ensure_thread_stops():
        time.sleep(0.5)
        gw.stop()
    t = threading.Thread(target=ensure_thread_stops)
    t.start()

    gw.running = True
    gw.run()


def test_start():
    message_queue = queue.Queue()
    Gateway.MIN_RECONNECTION_WAIT = 0.05
    Gateway.MAX_RECONNECTION_WAIT = 0.05

    gw = Gateway("SENSITIVE_INFO_TOKEN", message_queue, MockConnection)

    def run(gw):
        gw.started = True
    gw.run = run.__get__(gw, Gateway)

    def ensure_thread_stops():
        time.sleep(0.5)
        gw.stop()
    t = threading.Thread(target=ensure_thread_stops)
    t.start()

    gw.start()
    assert gw.running
    time.sleep(0.2)
    assert gw.started
