from discord import Message


def say(command_message, database, what_to_say, *args):
    """Makes Charlotte say something.

    Args:
        what_to_say: The content of the message Charlotte will send.

    Returns:
        A discord message.
    """
    response = Message(what_to_say, command_message.channel_id, "Charlotte", "Charlotte")
    return response
