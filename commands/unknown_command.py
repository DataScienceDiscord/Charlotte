from discord import Message


def unknown_command(message, database, *args):
    response = Message("There is no such command.", message.channel_id, "Charlotte", "Charlotte")
    return response
