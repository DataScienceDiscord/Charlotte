from discord import Message


def unknown_command(message, database):
    response = Message("There is no such command.", message.channel_id, "Charlotte", "Charlotte")
    return response
