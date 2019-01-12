import discord
from commands import top
from collections import namedtuple
import io


MockMessage = namedtuple("Message", ["channel_id", "content"])


MockUser = namedtuple("User", ["count", "username"])


class MockDatabase(object):

    def __init__(self):
        pass

    def get_top_members_per_message_count(self, top_n):
        users = []
        for i in range(top_n):
            user = MockUser(i, "user%d" % i)
            users.append(user)
        return users


def test_top_too_many_users():
    incoming_message = MockMessage("my_channel_id_123", "!c/top/10000")
    result = top(incoming_message, None, 10000)

    assert isinstance(result, discord.Message)
    assert result.content == "Fuck off mate, bandwidth ain't free."
    assert result.channel_id == incoming_message.channel_id


def test_top():
    incoming_message = MockMessage("my_channel_id_123", "!c/top/10000")
    db = MockDatabase()
    result = top(incoming_message, db, 5)

    assert isinstance(result, discord.Message)
    assert result.content == ""
    assert result.channel_id == incoming_message.channel_id
    assert result.attachment != None
    assert len(result.attachment) == 2
    assert result.attachment[0] == "top.png"
    assert isinstance(result.attachment[1], io.BytesIO)
