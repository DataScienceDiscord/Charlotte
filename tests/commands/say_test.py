import discord
from commands import say
from collections import namedtuple


Message = namedtuple("Message", ["channel_id", "content"])


def test_say():
    incoming_message = Message("my_channel_id_123", "!c/say/hello")

    result = say(incoming_message, None, "hello")

    assert isinstance(result, discord.Message)
    assert result.content == "hello"
    assert result.channel_id == incoming_message.channel_id
