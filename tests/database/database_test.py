import pytest
import datetime
from collections import namedtuple

from database import Database
from database import User
from database import Message

import database.config
assert database.config.ENV == "TEST"

MockMessage = namedtuple("Message", ["content",
                                     "channel_id",
                                     "user",
                                     "timestamp"])

@pytest.fixture()
def db():
    db = Database()
    yield db
    user_id = "1234edfg"
    messages = db.get_messages_for_user(user_id)
    for message in messages:
        db.delete_message(message.id)
    db.delete_user(user_id)


def test_add_user(db):
    # Setup
    user_id = "1234edfg"
    name = "name#1234"
    assert not db.user_exists(user_id)

    # Test
    assert db.add_user(user_id, name)
    user = db.get_user(user_id)
    assert user.user_id  == user_id
    assert user.username == name

    # Cleanup
    assert db.delete_user(user_id)


def test_user_exists(db):
    # Setup
    user_id = "1234edfg"
    name = "name#1234"
    db.add_user(user_id, name)

    # Test
    assert db.user_exists(user_id)
    assert not db.user_exists("nonexistantid")

    # Cleanup
    assert db.delete_user(user_id)


def test_delete_user(db):
    # Setup
    user_id = "1234edfg"
    name = "name#1234"
    db.add_user(user_id, name)
    assert db.user_exists(user_id)

    # Test
    assert db.delete_user(user_id) == True
    assert not db.user_exists(user_id)


def test_add_message(db):
    # Setup
    user_id = "1234edfg"
    name = "name#1234"
    db.add_user(user_id, name)

    content    = "This is a message, 1234#(- Hello."
    channel_id = "132456"
    user       = user_id
    date       = datetime.datetime.now()
    message = MockMessage(content, channel_id, user, date)

    # Test
    message = db.add_message(message)
    message = db.get_message(message.id)
    assert message.content      == content
    assert message.channel_id   == channel_id
    assert message.user.user_id == user
    assert message.date         == date

    # Cleanup
    assert db.delete_message(message.id)
    assert db.delete_user(user_id)


def test_delete_message(db):
    # Setup
    user_id = "1234edfg"
    name = "name#1234"
    db.add_user(user_id, name)

    content    = "This is a message, 1234#(- Hello."
    channel_id = "132456"
    user       = user_id
    date       = datetime.datetime.now()
    message = MockMessage(content, channel_id, user, date)
    message = db.add_message(message)

    # Test
    assert db.delete_message(message.id)
    assert not db.get_message(message.id)

    # Cleanup
    assert db.delete_user(user_id)

def test_get_messages_for_user(db):
    # Setup
    user_id = "1234edfg"
    name = "name#1234"
    db.add_user(user_id, name)

    content1    = "This is a message, 1234#(- Hello1."
    channel_id1 = "1324561"
    user1       = user_id
    date1       = datetime.datetime.now()
    message1 = MockMessage(content1, channel_id1, user1, date1)
    message1 = db.add_message(message1)

    content2    = "This is a message, 1234#(- Hello2."
    channel_id2 = "1324562"
    user2       = user_id
    date2       = datetime.datetime.now()
    message2 = MockMessage(content2, channel_id2, user2, date2)
    message2 = db.add_message(message2)

    # Test
    message1, message2 = db.get_messages_for_user(user_id)
    assert message1.content      == content1
    assert message1.channel_id   == channel_id1
    assert message1.user.user_id == user1
    assert message1.date         == date1
    assert message2.content      == content2
    assert message2.channel_id   == channel_id2
    assert message2.user.user_id == user2
    assert message2.date         == date2

    # Cleanup
    assert db.delete_message(message1.id)
    assert db.delete_message(message2.id)
    assert db.delete_user(user_id)
