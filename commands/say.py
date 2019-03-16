from discord import Message


def say(command_message, database, what_to_say, *args):
    response = Message(what_to_say, command_message.channel_id, "Charlotte", "Charlotte")
    return response
