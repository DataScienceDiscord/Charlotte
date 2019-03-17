from discord import Message


def unknown_command(message, database, *args):
    """Informs the user that the command was malformed or doesn't exist.

    Returns:
        A discord message.
    """
    response = Message("There is no such command.", message.channel_id, "Charlotte", "Charlotte")
    return response
