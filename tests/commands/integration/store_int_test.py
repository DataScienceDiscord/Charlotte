import pytest
import datetime

from discord import Message
from discord import Payload
from database import Database
from commands import store


import database.config
assert database.config.ENV == "TEST"


@pytest.fixture()
def db():
    db = Database()
    yield db
    member_id = "181098168266653698"
    messages = db.get_messages_for_member(member_id)
    for message in messages:
        db.delete_message(message.id)
    db.delete_member(member_id)


def test_store(db):

    # Test non-existant member
    packet = ' {"t":"MESSAGE_CREATE","s":6,"op":0,"d":{"type":0,"tts":false,"timestamp":"2019-01-12T02:05:59.275000+00:00","pinned":false,"nonce":"533466598925664256","mentions":[],"mention_roles":[],"mention_everyone":false,"member":{"roles":[],"mute":false,"joined_at":"2018-12-14T14:18:16.822000+00:00","deaf":false},"id":"533466644060831764","embeds":[],"edited_timestamp":null,"content":"hello there","channel_id":"523141683379175426","author":{"username":"Et","id":"181098168266653698","discriminator":"5175","avatar":"7625f24396b5fad487d5b90d36315032"},"attachments":[],"guild_id":"523141683379175424"}}'
    payload = Payload.from_packet(packet)
    message = Message.from_payload(payload)

    store(message, db)

    # Test existing member
    packet = ' {"t":"MESSAGE_CREATE","s":6,"op":0,"d":{"type":0,"tts":false,"timestamp":"2019-01-12T02:05:59.275000+00:00","pinned":false,"nonce":"533466598925664256","mentions":[],"mention_roles":[],"mention_everyone":false,"member":{"roles":[],"mute":false,"joined_at":"2018-12-14T14:18:16.822000+00:00","deaf":false},"id":"533466644060831764","embeds":[],"edited_timestamp":null,"content":"hello there","channel_id":"523141683379175426","author":{"username":"Et","id":"181098168266653698","discriminator":"5175","avatar":"7625f24396b5fad487d5b90d36315032"},"attachments":[],"guild_id":"523141683379175424"}}'
    payload = Payload.from_packet(packet)
    message = Message.from_payload(payload)

    store(message, db)
