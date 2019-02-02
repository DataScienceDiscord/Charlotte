import logging
import websocket
from discord.payload import Payload
from discord.gateway_exceptions import DisconnectionException


class GatewayConnection(object):
    ENDPOINT = "wss://gateway.discord.gg/?v=6&encoding=json"

    def __init__(self, wslib=websocket, logging=logging):
        self.wslib    = wslib
        self.ws       = wslib.WebSocket()
        self.last_seq = None
        self.logger   = logging.getLogger(__name__)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.logger.critical("Exiting connection context.", exc_info=(type, value, traceback))
        self.close()

    @property
    def endpoint(self):
        return GatewayConnection.ENDPOINT

    @property
    def connected(self):
        return self.ws.connected

    def open(self):
        """Opens a websocket connection to the gateway.

        raises:
            ValueError: When the gateway connection is already open.
        """
        self.logger.info("Creating new websocket.")
        if self.ws.connected:
            raise ValueError("Gateway connection already open.")
        self.ws.connect(self.endpoint)

    def close(self):
        """Closes the websocket connection."""
        self.logger.info("Closing gateway websocket.")
        self.ws.close()

    def receive_payload(self):
        """Receives a payload packet from the websocket
        and stores its sequence number.

        Returns:
            A Payload object.
        """
        packet = self.ws.recv()
        self.logger.info("Inc. packet: %s", packet[:1000])
        if packet == "":
            raise DisconnectionException()
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
        self.ws.send(packet)
        # Make sure we don't log confidential info.
        to_log = packet
        if payload.opcode == Payload.IDENTIFY or payload.opcode == Payload.RESUME:
            to_log = "CENSORED_PACKET_%d" % payload.opcode
        self.logger.info("Out. packet: %s", to_log)
