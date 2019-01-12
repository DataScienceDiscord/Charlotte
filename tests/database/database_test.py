import pytest
import datetime
from collections import namedtuple

from database import Database
from database import Member
from database import Message

import database.config
assert database.config.ENV == "TEST"

MockMessage = namedtuple("Message", ["content",
                                     "channel_id",
                                     "author_id",
                                     "timestamp"])

@pytest.fixture()
def db():
    db = Database()
    yield db
    member_id = "1234edfg"
    messages = db.get_messages_for_member(member_id)
    for message in messages:
        db.delete_message(message.id)
    db.delete_member(member_id)


def test_add_member(db):
    # Setup
    member_id = "1234edfg"
    name = "name#1234"
    assert not db.member_exists(member_id)

    # Test
    assert db.add_member(member_id, name)
    member = db.get_member(member_id)
    assert member.member_id  == member_id
    assert member.username == name

    # Cleanup
    assert db.delete_member(member_id)


def test_member_exists(db):
    # Setup
    member_id = "1234edfg"
    name = "name#1234"
    db.add_member(member_id, name)

    # Test
    assert db.member_exists(member_id)
    assert not db.member_exists("nonexistantid")

    # Cleanup
    assert db.delete_member(member_id)


def test_delete_member(db):
    # Setup
    member_id = "1234edfg"
    name = "name#1234"
    db.add_member(member_id, name)
    assert db.member_exists(member_id)

    # Test
    assert db.delete_member(member_id) == True
    assert not db.member_exists(member_id)


def test_add_message(db):
    # Setup
    member_id = "1234edfg"
    name = "name#1234"
    db.add_member(member_id, name)

    content    = "This is a message, 1234#(- Hello."
    channel_id = "132456"
    member     = member_id
    date       = datetime.datetime.now()
    message = MockMessage(content, channel_id, member, date)

    # Test
    message = db.add_message(message)
    message = db.get_message(message.id)
    assert message.content      == content
    assert message.channel_id   == channel_id
    assert message.member.member_id == member
    assert message.date         == date

    # Cleanup
    assert db.delete_message(message.id)
    assert db.delete_member(member_id)


def test_delete_message(db):
    # Setup
    member_id = "1234edfg"
    name = "name#1234"
    db.add_member(member_id, name)

    content    = "This is a message, 1234#(- Hello."
    channel_id = "132456"
    member     = member_id
    date       = datetime.datetime.now()
    message = MockMessage(content, channel_id, member, date)
    message = db.add_message(message)

    # Test
    assert db.delete_message(message.id)
    assert not db.get_message(message.id)

    # Cleanup
    assert db.delete_member(member_id)

def test_get_messages_for_member(db):
    # Setup
    member_id = "1234edfg"
    name = "name#1234"
    db.add_member(member_id, name)

    content1    = "This is a message, 1234#(- Hello1."
    channel_id1 = "1324561"
    member1     = member_id
    date1       = datetime.datetime.now()
    message1 = MockMessage(content1, channel_id1, member1, date1)
    message1 = db.add_message(message1)

    content2    = "This is a message, 1234#(- Hello2."
    channel_id2 = "1324562"
    member2       = member_id
    date2       = datetime.datetime.now()
    message2 = MockMessage(content2, channel_id2, member2, date2)
    message2 = db.add_message(message2)

    # Test
    message1, message2 = db.get_messages_for_member(member_id)
    assert message1.content      == content1
    assert message1.channel_id   == channel_id1
    assert message1.member.member_id == member1
    assert message1.date         == date1
    assert message2.content      == content2
    assert message2.channel_id   == channel_id2
    assert message2.member.member_id == member2
    assert message2.date         == date2

    # Cleanup
    assert db.delete_message(message1.id)
    assert db.delete_message(message2.id)
    assert db.delete_member(member_id)
