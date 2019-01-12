import queue
from dispatcher import Dispatcher
from collections import namedtuple
from discord import Message
import time


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


def test_process_message_not_a_command():
    Commands = namedtuple("Commands", ["identifiers"])
    def command_func(message, database, arg1, arg2, arg3):
        return message, database, arg1, arg2, arg3

    stored = False
    def store(message, database):
        nonlocal stored
        stored = True

    commands = Commands({"store": store})

    consumer = MockConsumer()

    ds = Dispatcher(queue.Queue(), "database", "consumer", commands)
    message = Message("hello", "channel_id", "user", "username")
    ds.process_message(message)
    assert stored


def test_process_message_command():
    Commands = namedtuple("Commands", ["identifiers"])

    def command_func(message, database, param):
        return message, database, param
    commands = Commands({"existing_command": command_func,
                         "store": lambda *args, **kwargs: None})

    consumer = MockConsumer()

    ds = Dispatcher(queue.Queue(), "database", consumer, commands)
    message = Message("!c/existing_command/myparam", "channel_id", "user", "username")
    ds.process_message(message)
    assert consumer.create_message_called
    assert consumer.message_created == (message, "database", "myparam")


def test_process_message_unknown_command():
    Commands = namedtuple("Commands", ["identifiers"])

    unknown_called = False
    def unknown_command(message, database, *args):
        nonlocal unknown_called
        unknown_called = True
        return "Response I expect to send."

    commands = Commands({"unknown_command": unknown_command,
                         "store": lambda *args, **kwargs: None})

    consumer = MockConsumer()

    ds = Dispatcher(queue.Queue(), "database", consumer, commands)
    message = Message("!c/not_an_actual_command/myparam", "channel_id", "user", "username")
    ds.process_message(message)
    assert unknown_called
    assert consumer.create_message_called
    assert consumer.message_created == "Response I expect to send."


def test_start_run_stop():
    Commands = namedtuple("Commands", ["identifiers"])

    unknown_called = False
    def unknown_command(message, database, *args):
        nonlocal unknown_called
        unknown_called = True
        return "Response I expect to send."

    commands = Commands({"unknown_command": unknown_command,
                         "store": lambda *args, **kwargs: None})

    consumer = MockConsumer()

    incoming_queue = queue.Queue()
    ds = Dispatcher(incoming_queue, "database", consumer, commands, queue_timeout=0.1)

    t = ds.start()
    assert t.is_alive()

    message = Message("!c/not_an_actual_command/myparam", "channel_id", "user", "username")
    incoming_queue.put(message)

    time.sleep(0.2)
    assert unknown_called
    assert consumer.create_message_called
    assert consumer.message_created == "Response I expect to send."

    ds.stop()
    time.sleep(0.3)
    assert not t.is_alive()


    t = ds.start()
    assert t.is_alive()

    incoming_queue.put(None)
    time.sleep(0.3)

    assert not t.is_alive()
