import commands
from discord import Message


def help(message, database, *args):
    """Displays the list of commands or the documentation for a specific command.

    Args:
        command: The name of the command whose documentation must be displayed. If this
        parameter isn't given the list of commands will be displayed.

    Returns:
        A discord message.
    """
    if len(args) == 0 or args[0] == "":
        help_message = "```Commands: \n - " + "\n - ".join(commands.identifiers) + "```"
    elif args[0] in commands.identifiers:
        help_message = "```%s```" % commands.identifiers[args[0]].__doc__
    else:
        return commands.unknown_command(message, database, *args)
    response = Message(help_message, message.channel_id, "Charlotte", "Charlotte")
    return response
