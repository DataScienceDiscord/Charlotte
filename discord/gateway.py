import time
import threading

from discord.payload import Payload
from discord.message import Message


class Gateway(object):
    """An interface for discord's gateway API as described here:
    https://discordapp.com/developers/docs/topics/gateway

    Args:
        token: The bot token.
        message_queue: An empty queue that the gateway will dispatch received messages into.
        wslib: A websocket library.
    """
    ENDPOINT = "wss://gateway.discord.gg/?v=6&encoding=json"
    DEFAULT_HEARTBEAT_PERIOD = 45 # seconds
    OS = "linux"
    NAME = "Charlotte"
    RECONNECTION_FAILURE_THRESHOLD = 3
    RECONNECTION_COUNTER_RESET     = 600

    def __init__(self, token, message_queue, wslib):
        self.token = token
        self.message_queue = message_queue
        self.wslib     = wslib
        self.running   = False
        self.connected = False
        self.heartbeat_period = Gateway.DEFAULT_HEARTBEAT_PERIOD
        self.heartbeat_acknowledged = True
        self.last_seq          = None
        self.session_id        = None
        self.reconnect_counter = 0
        self.last_reconnect    = time.time()

    @property
    def endpoint(self):
        return Gateway.ENDPOINT

    @property
    def time_since_last_reconnect(self):
        return time.time() - self.last_reconnect

    def receive_payload(self):
        """Receives a payload packet from the websocket
        and stores its sequence number.

        Returns:
            A Payload object.
        """
        packet = self.ws.recv()
        if packet == "":
            return None
        print("<<", packet)
        payload = Payload.from_packet(packet)
        if payload.seq_number:
            self.last_seq = payload.seq_number
        return payload

    def send_payload(self, payload):
        """Sends a payload packet to the gateway.

        Args:
            payload: A Payload object.
        """
        packet = payload.to_packet()
        print(">>", packet)
        self.ws.send(packet)

    def perform_handshake(self):
        """Waits for the gateway to say hello then identifies with it and
        waits for its READY acknowledgment.
        In the process the heartbeat interval and session ID are defined.

        Raises:
            AssertionError: Unexpected behaviour from the gateway during the handshake.
            KeyError: Handshake messages did not contain necessary information.
        """
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
        """Opens a connection to the gateway and perform the agreed upon handshake.

        Raises:
            AssertionError: Unexpected behaviour from the gateway during the handshake.
            KeyError: Handshake messages did not contain necessary information.
        """
        self.ws = self.wslib.WebSocket()
        self.ws.connect(self.endpoint)

        try:
            self.perform_handshake()
        except (AssertionError, KeyError):
            self.ws.close()
            raise

    def resume(self):
        """Attempts to reopen a connection and send a RESUME Payload to
        get all the events that were sent during the disconnection period.

        In the event that it fails to connect the first time,
        it will attempt to open a new connection without resuming from the last
        message received.

        Raises:
            AssertionError: Unexpected behaviour from the gateway during the handshake.
            KeyError: Handshake messages did not contain necessary information.
        """
        try:
            self.connect()
        except AssertionError: # TODO: Move this outside resume
            # "It's also possible that your client cannot reconnect in time to resume,
            # in which case the client will receive a Opcode 9 Invalid Session and is expected
            # to wait a random amount of time—between 1 and 5 seconds—then send a fresh Opcode 2 Identify.
            time.sleep(5)
            self.connect()
            return
        payload = Payload.Resume(self.token, self.session_id, self.last_seq)
        self.send_payload(payload)

    def reconnect(self):
        """Closes the current connection and attempts to open a new one
        and resume at the last message received.

        Raises:
            AssertionError: Unexpected behaviour from the gateway during the handshake.
            KeyError: Handshake messages did not contain necessary information.
        """
        self.stop()
        self.close()
        time.sleep(5)
        if self.reconnect_counter >= Gateway.RECONNECTION_FAILURE_THRESHOLD:
            raise ValueError("Reconnection attempts threshold has been reached. Stopping.")
        self.resume()
        self.start()
        self.reconnect_counter += 1
        self.last_reconnect     = time.time()

    def send_heartbeat(self):
        """Sends a single HEARTBEAT Payload to the gateway."""
        self.heartbeat_acknowledged = False
        payload = Payload(Payload.HEARTBEAT, data=self.last_seq)
        self.send_payload(payload)

    def make_heart_beat(self):
        """Sends heartbeats at the chosen heartbeat interval
        until told to stop or the connection drops, in which case
        it'll attempt to reconnect.
        """
        while self.running:
            if not self.heartbeat_acknowledged:
                self.reconnect()
                break

            if self.reconnect_counter > 0 and self.time_since_last_reconnect >= Gateway.RECONNECTION_COUNTER_RESET:
                self.reconnect_counter = 0

            self.send_heartbeat()
            time.sleep(self.heartbeat_period)

    def run(self):
        """Receives and handle payloads until told to stop or the connection drops.
        When a DISPATCH Payload is received it'll be put inside the message queue
        for further processing by listeners.
        """
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
        """Closes the websocket connection."""
        self.ws.close()

    def start(self):
        """Starts listening for Payloads and sending heartbeats."""
        self.running = True
        t = threading.Thread(target=self.run)
        t.start()
        t = threading.Thread(target=self.make_heart_beat)
        t.start()

    def stop(self):
        """Stops listening for Payloads and sending heartbeats."""
        self.running = False
