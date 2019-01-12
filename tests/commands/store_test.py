import discord
from commands import store
from collections import namedtuple


MockMessage = namedtuple("Message", ["content",
                                     "channel_id",
                                     "author_id",
                                     "username"])


MockUser = namedtuple("User", ["count", "username"])


class MockDatabase(object):

    def __init__(self, user_exists_flag):
        self.user_exists_flag = user_exists_flag
        self.added_user = None
        self.added_message = None

    def member_exists(self, user):
        if self.user_exists_flag:
            return True
        return False

    def add_member(self, user, username):
        self.added_user = (user, username)

    def add_message(self, message):
        self.added_message = message


def test_store_new_user():
    user = "generalkenobi#1234"
    username = "kenboy"

    message = MockMessage("Hello there!",
                          "my_channel_id_123",
                          user,
                          username)

    db = MockDatabase(user_exists_flag=False)
    store(message, db)

    assert db.added_user != None
    stored_user, stored_username = db.added_user
    assert stored_user == message.user
    assert stored_username == message.username
    assert db.added_message == message


def test_store_user_exists():
    user = "generalkenobi#1234"
    username = "kenboy"

    message = MockMessage("Hello there!",
                          "my_channel_id_123",
                          user,
                          username)

    db = MockDatabase(user_exists_flag=True)
    store(message, db)

    assert db.added_user == None
    assert db.added_message == message
