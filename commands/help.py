import commands
from discord import Message


def help(message, database, *args):
    if len(args) == 0:
        help_message = "```Commands: \n - " + "\n - ".join(commands.identifiers) + "```"
    elif args[0] in commands.identifiers:
        help_message = "```%s```" % commands.identifiers[args[0]].__doc__
    else:
        return commands.unknown_command(message, database, *args)
    response = Message(help_message, message.channel_id, "Charlotte", "Charlotte")
    return response
