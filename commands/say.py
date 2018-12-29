from discord import Message


def say(what_to_say, command_message, database):
    response = Message(what_to_say, command_message.channel_id, "Charlotte", "Charlotte")
    return response
