import time
import threading
import logging

from discord.payload import Payload
from discord.message import Message
from discord.gateway_exceptions import DisconnectionException
from discord.gateway_exceptions import InvalidSessionException
from discord.gateway_connection import GatewayConnection

class Gateway(object):
    """An interface for discord's gateway API as described here:
    https://discordapp.com/developers/docs/topics/gateway

    Args:
        token: The bot token.
        message_queue: An empty queue that the gateway will dispatch received messages into.
        wslib: A websocket library.
    """
    DEFAULT_HEARTBEAT_PERIOD = 45 # seconds
    OS = "linux"
    NAME = "Charlotte"
    MIN_RECONNECTION_WAIT = 5 # seconds
    MAX_RECONNECTION_WAIT = 30 * 60 # seconds

    def __init__(self, token, message_queue, GatewayConnection=GatewayConnection, logging=logging):
        self.message_queue = message_queue
        self.GatewayConnection = GatewayConnection

        self.token = token
        self.session_id       = None
        self.heartbeat_period = Gateway.DEFAULT_HEARTBEAT_PERIOD

        self.running = False
        self.reconnect_counter = 0

        self.last_beat = 0
        self.last_ack  = 0

        self.logger = logging.getLogger(__name__)

    @property
    def connection_interval(self):
        return min(2**self.reconnect_counter + Gateway.MIN_RECONNECTION_WAIT, Gateway.MAX_RECONNECTION_WAIT)

    def perform_handshake(self, connection, resume=False):
        """Waits for the gateway to say hello then identifies with it and
        waits for its READY acknowledgment.
        In the process the heartbeat interval and session ID are defined.

        Raises:
            AssertionError: Unexpected behaviour from the gateway during the handshake.
            KeyError: Handshake messages did not contain necessary information.
        """
        payload = connection.receive_payload()
        assert payload == Payload.HELLO, "First message upon connection was not HELLO."
        self.heartbeat_period = payload.data["heartbeat_interval"] / 1000

        # Identify
        if resume:
            payload = Payload.Resume(self.token, self.session_id, connection.last_seq)
        else:
            payload = Payload.Identify(self.token, self.OS, self.NAME)
        connection.send_payload(payload)

        # Get ready
        payload = connection.receive_payload()
        if payload == Payload.DISPATCH and payload.event_name == "READY":
            self.session_id = payload.data["session_id"]
        elif payload == Payload.INVALID:
            raise InvalidSessionException()
        else:
            self.process_payload(payload, connection)

    def send_heartbeat(self, connection):
        payload = Payload(Payload.HEARTBEAT, data=connection.last_seq)
        connection.send_payload(payload)

    def send_heartbeats(self, connection):
        """Sends heartbeats at the chosen heartbeat interval
        until told to stop or the connection drops, in which case
        it'll attempt to reconnect.
        """
        self.logger.info("Heartbeat loop started.")
        self.last_ack  = time.time()
        self.last_beat = time.time()
        while self.running and connection.connected:
            if self.last_beat - self.last_ack > self.heartbeat_period: # FUCKED HERE
                self.logger.info("Heart skipped a beat.")
                # Closing the connection in the heartbeat thread
                # will make the processing thread receive an
                # empty packet and attempt a reconnect
                connection.close()
                break

            self.send_heartbeat(connection)
            self.last_beat = time.time()
            time.sleep(self.heartbeat_period)
        self.logger.info("Heartbeat loop ended.")

    def process_payload(self, payload, connection):
        if payload == Payload.HEARTBEAT:
            self.send_heartbeat(connection)

        elif payload == Payload.HEARTBEAT_ACK:
            self.last_ack = time.time()

        elif payload == Payload.DISPATCH and payload.event_name == "MESSAGE_CREATE":
            message = Message.from_payload(payload)
            self.message_queue.put(message)

    def process_payloads(self, connection):
        self.logger.info("Gateway payload processing started.")
        while self.running and connection.connected:
            try:
                payload = connection.receive_payload()
                self.process_payload(payload, connection)
            except DisconnectionException:
                self.logger.exception("Gateway disconnected.")
                break
        self.logger.info("Gateway payload processing ended.")

    def run(self):
        """Receives and handle payloads until told to stop or the connection drops.
        When a DISPATCH Payload is received it'll be put inside the message queue
        for further processing by listeners.
        """
        self.logger.info("Gateway main thread starting.")
        resuming = False
        while self.running:
            time.sleep(self.connection_interval)
            with self.GatewayConnection() as connection:
                try:
                    self.perform_handshake(connection, resuming)
                except InvalidSessionException:
                    self.logger.info("Gateway couldn't resume in time.")
                    resuming = False
                    continue
                except DisconnectionException:
                    self.logger.info("Gateway disconnected during handshake.")
                    continue

                t = threading.Thread(target=self.send_heartbeats, args=[connection])
                t.start()

                self.reconnect_counter = 0
                self.process_payloads(connection)

            self.reconnect_counter += 1
            resuming = True
        self.logger.info("Gateway main thread exiting.")

    def start(self):
        """Starts listening for Payloads and sending heartbeats."""
        self.running = True
        t = threading.Thread(target=self.run)
        t.start()

    def stop(self):
        """Stops listening for Payloads and sending heartbeats."""
        self.running = False
