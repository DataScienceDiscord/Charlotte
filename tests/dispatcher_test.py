import queue
from dispatcher import Dispatcher
from collections import namedtuple
from discord import Message


class MockConsumer(object):

    def __init__(self):
        self.create_message_called = False
        self.message_created = None

    def create_message(self, message):
        self.create_message_called = True
        self.message_created = message


def test_is_command():
    ds = Dispatcher(queue.Queue(), None, None, None)

    content = "!c/say/hello"
    assert ds.is_command(content)

    content = "!c/dice"
    assert ds.is_command(content)

    content = "#c/say/hello"
    assert not ds.is_command(content)

    content = "c!/say/hello"
    assert not ds.is_command(content)

    content = "sqegfqs<!//!cg"
    assert not ds.is_command(content)

    content = "sqegfqs!c/"
    assert not ds.is_command(content)


def test_parse():
    ds = Dispatcher(queue.Queue(), None, None, None)

    content = "!c/say/hello"
    command, params = ds.parse(content)
    assert command == "say"
    assert params == "hello"

    content = "!c/dice"
    command, params = ds.parse(content)
    assert command == "dice"
    assert params == ""

    content = "!c/"
    try:
        command, params = ds.parse(content)
        assert False, "Should have raised a BadCommandError."
    except ValueError:
        pass

    content = "dfgswrg"
    command, params = ds.parse(content)
    assert command == None
    assert params == None


def test_dispatch():
    Commands = namedtuple("Commands", ["identifiers"])
    def command_func(message, database, arg1, arg2, arg3):
        return message, database, arg1, arg2, arg3
    commands = Commands({"existing_command": command_func})

    ds = Dispatcher(queue.Queue(), "database", "consumer", commands)

    # Correct args
    response = ds.dispatch("existing_command",
                           "message",
                           "arg1",
                           "arg2",
                           "arg3")
    assert response == ("message", "database", "arg1", "arg2", "arg3")


    # Wrong args, correct command
    try:
        response = ds.dispatch("existing_command",
                               "message",
                               "arg1",
                               "arg2")
        assert False, "Should have raised a TypeError."
    except TypeError:
        pass


    # Wrong command
    try:
        response = ds.dispatch("wrong_command", "message", "database")
        assert False, "Should have raised a KeyError."
    except KeyError:
        pass


def test_process_message():
    Commands = namedtuple("Commands", ["identifiers"])
    def command_func(message, database, arg1, arg2, arg3):
        return message, database, arg1, arg2, arg3
    commands = Commands({"existing_command": command_func, "store": lambda *args, **kwargs: None})

    consumer = MockConsumer()


    ds = Dispatcher(queue.Queue(), "database", "consumer", commands)
    message = Message("hello", "channel_id", "user", "username")
    ds.process_message(message)
