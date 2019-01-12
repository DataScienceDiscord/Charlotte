from discord import Message
import datetime
from collections import namedtuple
import json


MockPayload = namedtuple("Payload", ["data"])


def test_from_payload():
    payload = MockPayload({
        "content": "hello",
        "channel_id": "my_channel_id123",
        "author": {
            "id": "1234",
            "username": "Django",
            "discriminator": "#1235"
        },
        "timestamp": datetime.datetime.now()
    })

    message = Message.from_payload(payload)

    assert isinstance(message, Message)
    assert message.content    == payload.data["content"]
    assert message.channel_id == payload.data["channel_id"]
    assert message.author_id  == payload.data["author"]["id"]
    assert message.username   == payload.data["author"]["username"] + "#" + payload.data["author"]["discriminator"]
    assert message.timestamp  == payload.data["timestamp"]


def test_to_payload():
    payload = MockPayload({
        "content": "hello",
        "channel_id": "my_channel_id123",
        "author": {
            "id": "1234",
            "username": "Django",
            "discriminator": "#1235"
        },
        "timestamp": datetime.datetime.now()
    })

    message = Message.from_payload(payload)
    new_payload = message.to_payload()

    assert new_payload["content"] == payload.data["content"]
    assert new_payload["tts"]     == False
    assert new_payload["embed"]   == message.embed


def test_to_json():
    payload = MockPayload({
        "content": "hello",
        "channel_id": "my_channel_id123",
        "author": {
            "id": "1234",
            "username": "Django",
            "discriminator": "#1235"
        },
        "timestamp": datetime.datetime.now()
    })

    message = Message.from_payload(payload)
    payload = message.to_payload()

    json_payload = message.to_json()

    reconstructed = json.loads(json_payload)

    assert payload == reconstructed
