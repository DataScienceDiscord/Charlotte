import discord
from commands import unknown_command
from collections import namedtuple


Message = namedtuple("Message", ["channel_id", "content"])


def test_say():
    incoming_message = Message("my_channel_id_123", "!c/sefkjlhef/hello")

    result = unknown_command(incoming_message, None)

    assert isinstance(result, discord.Message)
    assert result.content == "There is no such command."
    assert result.channel_id == incoming_message.channel_id
