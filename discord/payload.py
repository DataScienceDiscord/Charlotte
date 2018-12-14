import json


class Payload(object):
    """A discord gateway payload as described here:
    https://discordapp.com/developers/docs/topics/gateway#payloads

    Args:
        opcode: Opcode for the payload. (as described here: https://discordapp.com/developers/docs/topics/opcodes-and-status-codes#gateway-opcodes)
        data: A dictionary containing the payload data.
        seq_number: sequence number, used for resuming sessions and heartbeats.
        event_name: the event name for this payload.
    """
    DISPATCH      = 0
    HEARTBEAT     = 1
    IDENTIFY      = 2
    STATUS_UPDATE = 3
    VOICE_UPDATE  = 4
    RESUME        = 6
    RECONNECT     = 7
    REQUEST_MEMB  = 8
    INVALID       = 9
    HELLO         = 10
    HEARTBEAT_ACK = 11

    def __init__(self, opcode, data, seq_number=None, event_name=None):
        self.opcode = opcode
        self.data = data
        self.seq_number = seq_number
        self.event_name = event_name

    def __eq__(self, payload):
        if isinstance(payload, Payload):
            return payload.__dict__ == self.__dict__
        elif isinstance(payload, int):
            return self.opcode == payload
        return False

    def _compress(self):
        raise NotImplementedError()

    def _decompress(self):
        raise NotImplementedError()

    @staticmethod
    def from_packet(packet):
        json_payload = json.loads(packet)
        return Payload(opcode     = json_payload["op"],
                       data       = json_payload["d"],
                       seq_number = json_payload["s"],
                       event_name = json_payload["t"])

    def to_packet(self):
        packet = {
            "op": self.opcode,
            "d":  self.data,
            "s":  self.seq_number,
            "t":  self.event_name
        }
        return json.dumps(packet)

    @staticmethod
    def Resume(token, session_id, last_seq):
        data = {
            "token":      token,
            "session_id": session_id,
            "seq":        last_seq
        }
        return Payload(Payload.RESUME, data)

    @staticmethod
    def Identify(token, os, name):
        data = {
            "token": token,
            "properties": {
                "$os":      os,
                "$browser": name,
                "$device":  name
            }
        }
        return Payload(Payload.IDENTIFY, data)
