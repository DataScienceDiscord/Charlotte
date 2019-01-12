import pytest
import datetime

from discord import Message
from discord import Payload
from database import Database
from commands import top


import database.config
assert database.config.ENV == "TEST"


@pytest.fixture()
def db():
    db = Database()
    for i in range(10):
        member_id = "member%d"   % i
        username  = "username%d" % i
        db.add_member(member_id, username)
        for j in range(i*2):
            content = "content%d-%d" % (i, j)
            channel_id = "channel_id1234"
            message = Message(content, channel_id, member_id, username, datetime.datetime.now())
            db.add_message(message)
    yield db
    for i in range(10):
        member_id = "member%d"   % i
        username  = "username%d" % i
        messages = db.get_messages_for_member(member_id)
        for message in messages:
            db.delete_message(message.id)
        db.delete_member(member_id)


def test_top(db):

    packet = '{"t":"MESSAGE_CREATE","s":5,"op":0,"d":{"type":0,"tts":false,"timestamp":"2019-01-12T01:42:21.512000+00:00","pinned":false,"nonce":"533460652941901824","mentions":[],"mention_roles":[],"mention_everyone":false,"member":{"roles":[],"mute":false,"joined_at":"2018-12-14T14:18:16.822000+00:00","deaf":false},"id":"533460697531809803","embeds":[],"edited_timestamp":null,"content":"!c/top/9","channel_id":"523141683379175426","author":{"username":"Et","id":"181098168266653698","discriminator":"5175","avatar":"7625f24396b5fad487d5b90d36315032"},"attachments":[],"guild_id":"523141683379175424"}}'
    payload = Payload.from_packet(packet)
    message = Message.from_payload(payload)

    top(message, db, 5)
