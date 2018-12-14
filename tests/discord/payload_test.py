from discord import Payload


def test_create_payload_from_packet():
    PAYLOAD = '{"t":null,"s":null,"op":10,"d":{"heartbeat_interval":41250,"_trace":["gateway-prd-main-bwx0"]}}'
    payload = Payload.from_packet(PAYLOAD)
    assert payload.opcode == 10
    assert payload.seq_number == None
    assert payload.data == {"heartbeat_interval":41250, "_trace":["gateway-prd-main-bwx0"]}
    assert payload.event_name == None

    PAYLOAD = '{"t":"GATEWAY_EVENT_NAME","s":42,"op":0,"d":{}}'
    payload = Payload.from_packet(PAYLOAD)
    assert payload.opcode == 0
    assert payload.seq_number == 42
    assert payload.data == {}
    assert payload.event_name == "GATEWAY_EVENT_NAME"


def test_equality_operator():
    payload = Payload(opcode=10,
                      data={"hello":"world"},
                      seq_number=20,
                      event_name="Hello")

    assert payload == 10
    assert payload != 11

    payload2 = Payload(opcode=10,
                      data={"hello":"world"},
                      seq_number=20,
                      event_name="Hello")

    assert payload2 == payload

    payload2.opcode = 11
    assert payload2 != payload

    payload2.opcode = payload.opcode
    payload2.seq_number = 21
    assert payload2 != payload

    payload2.seq_number = payload.seq_number
    payload2.event_name = "Not Hello"
    assert payload2 != payload

    payload2.event_name = payload.event_name
    payload2.data = {"hello":"not world"}
    assert payload2 != payload

    payload2.data = payload.data
    assert payload2 == payload
