import os
import commands


def test_command_identifiers():
    command_modules = [m for m in os.listdir("commands") if ".py" in m]

    num_commands = len(command_modules) - 1 # -1 for __init__
    assert num_commands == len(commands.identifiers)
