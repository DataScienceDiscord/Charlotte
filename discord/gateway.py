import time
import threading

from discord.payload import Payload
from discord.message import Message


class Gateway(object):
    ENDPOINT = "wss://gateway.discord.gg/?v=6&encoding=json"
    DEFAULT_HEARTBEAT_PERIOD = 45 # seconds
    OS = "linux"
    NAME = "Charlotte"
    ENV = "DEV"

    def __init__(self, token, message_queue, wslib):
        self.token = token
        self.message_queue = message_queue
        self.wslib     = wslib
        self.running   = False
        self.connected = False
        self.heartbeat_period = Gateway.DEFAULT_HEARTBEAT_PERIOD
        self.heartbeat_acknowledged = True
        self.last_seq         = None
        self.session_id       = None
        self.GUILD = "523141683379175424" if Gateway.ENV == "DEV" else "464539978442211328"

    @property
    def endpoint(self):
        return Gateway.ENDPOINT

    def receive_payload(self):
        packet = self.ws.recv()
        if packet == "":
            return None
        print("<<", packet)
        payload = Payload.from_packet(packet)
        if payload.seq_number:
            self.last_seq = payload.seq_number
        return payload

    def send_payload(self, payload):
        packet = payload.to_packet()
        print(">>", packet)
        self.ws.send(packet)

    def perform_handshake(self):
        # Say hello
        payload = self.receive_payload()
        assert payload == Payload.HELLO, "First message upon connection was not HELLO."
        self.heartbeat_period = payload.data["heartbeat_interval"] / 1000
        # Identify
        payload = Payload.Identify(self.token, self.OS, self.NAME)
        self.send_payload(payload)
        # Get ready
        payload = self.receive_payload()
        assert payload == Payload.DISPATCH and payload.event_name == "READY", "Did not receive READY payload after IDENTIFY."
        self.session_id = payload.data["session_id"]

    def connect(self):
        self.ws = self.wslib.WebSocket()
        self.ws.connect(self.endpoint)

        try:
            self.perform_handshake()
        except (AssertionError, KeyError):
            self.ws.close()
            raise

    def resume(self):
        try:
            self.connect()
        except AssertionError:
            # "It's also possible that your client cannot reconnect in time to resume,
            # in which case the client will receive a Opcode 9 Invalid Session and is expected
            # to wait a random amount of time—between 1 and 5 seconds—then send a fresh Opcode 2 Identify.
            time.sleep(5)
            self.connect()
            return
        payload = Payload.Resume(self.token, self.session_id, self.last_seq)
        self.send_payload(payload)

    def reconnect(self):
        self.stop()
        self.close()
        time.sleep(5)
        self.resume()
        self.start()

    def send_heartbeat(self):
        self.heartbeat_acknowledged = False
        payload = Payload(Payload.HEARTBEAT, data=self.last_seq)
        self.send_payload(payload)

    def make_heart_beat(self):
        while self.running:
            if not self.heartbeat_acknowledged:
                self.reconnect()
                break

            self.send_heartbeat()
            time.sleep(self.heartbeat_period)

    def run(self):
        while self.running:
            payload = self.receive_payload()

            if payload == None:
                self.stop()
                self.close()
                raise ValueError("Connection closed.")

            elif payload == Payload.HEARTBEAT:
                self.send_heartbeat()
                # We don't require acknowledgement for requested beats
                # so as not to create race conditions with beating thread.
                self.heartbeat_acknowledged = True

            elif payload == Payload.HEARTBEAT_ACK:
                self.heartbeat_acknowledged = True

            elif payload == Payload.DISPATCH and payload.event_name == "MESSAGE_CREATE":
                message = Message.from_payload(payload)
                self.message_queue.put(message)

    def close(self):
        self.ws.close()

    def start(self):
        self.running = True
        t = threading.Thread(target=self.run)
        t.start()
        t = threading.Thread(target=self.make_heart_beat)
        t.start()

    def stop(self):
        self.running = False
