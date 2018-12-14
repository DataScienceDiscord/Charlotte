import queue
from dispatcher import Dispatcher


def test_is_command():
    ds = Dispatcher(queue.Queue(), None, None)

    content = "!c:say:hello"
    assert ds.is_command(content)

    content = "!c:dice"
    assert ds.is_command(content)

    content = "#c:say:hello"
    assert not ds.is_command(content)

    content = "c!:say:hello"
    assert not ds.is_command(content)

    content = "sqegfqs<!::!cg"
    assert not ds.is_command(content)

    content = "sqegfqs!c:"
    assert not ds.is_command(content)

def test_parse():
    ds = Dispatcher(queue.Queue(), None, None)

    content = "!c:say:hello"
    command, params = ds.parse(content)
    assert command == "say"
    assert params == "hello"

    content = "!c:dice"
    command, params = ds.parse(content)
    assert command == "dice"
    assert params == ""

    content = "!c:"
    try:
        command, params = ds.parse(content)
        assert False, "Should have raised a BadCommandError."
    except ValueError:
        pass

    content = "dfgswrg"
    command, params = ds.parse(content)
    assert command == None
    assert params == None
