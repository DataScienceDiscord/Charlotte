from database import User
from database import Message
from peewee import fn, JOIN, SQL


class Database(object):
    """An interface to the bot's database."""

    def add_user(self, user_id, username):
        """Adds a user to the database.

        Args:
            user_id: Unique discord id for that user.
            username: Username and discriminator combination string.

        Returns:
            A user record.
        """
        user = User.create(user_id=user_id, username=username)
        return user

    def user_exists(self, user_id):
        """Checks whether the chosen user is present in the database.

        Args:
            user_id: Unique discord id for that user.

        Returns:
            Whether there is a user with that id in the database.
        """
        query = User.select().where(User.user_id == user_id)
        return query.exists()

    def get_user(self, user_id):
        """Gets a user from the database.

        Args:
            user_id: Unique discord id for that user.

        Returns:
            A user record.
        """
        return User.select().where(User.user_id == user_id).first()

    def delete_user(self, user_id):
        """Deletes a user from the database.

        Args:
            user_id: Unique discord id for that user.

        Returns:
            Whether the user was succesfully deleted.
        """
        return User.delete().where(User.user_id == user_id).execute()

    def add_message(self, message):
        """Adds a message to the database.

        Args:
            message: A discord message.

        Returns:
            A message record.
        """
        message = Message.create(content    = message.content,
                                 channel_id = message.channel_id,
                                 user       = message.user,
                                 date       = message.timestamp)
        return message

    def get_message(self, message_id):
        """Gets a message from the database.

        Args:
            message_id: The message's uid in the database.

        Returns:
            A message record.
        """
        return Message.select().where(Message.id == message_id).first()

    def get_messages_for_user(self, user_id):
        """Gets all messages for the chosen user.

        Args:
            user_id: Unique discord id for that user.

        Returns:
            A list of message records.
        """
        return list(Message.select().where(Message.user == user_id))

    def delete_message(self, message_id):
        """Deletes a message from the database.

        Args:
            message_id: The message's uid in the database.

        Returns:
            Whether the message was succesfully deleted.
        """
        return Message.delete().where(Message.id == message_id).execute()

    def get_top_users_per_message_count(self, top_n=9):
        query = User.select(User, fn.Count(Message.id).alias('count')) \
                    .join(Message, JOIN.RIGHT_OUTER) \
                    .group_by(User) \
                    .order_by(SQL('count').desc()) \
                    .limit(top_n)
        return list(query)

    def get_top_users_per_num_characters(self, top_n=20):
        query = User.select(User, fn.SUM(fn.LENGTH(Message.content)).alias('length')) \
                    .join(Message, JOIN.RIGHT_OUTER) \
                    .group_by(User) \
                    .order_by(SQL('length').desc()) \
                    .limit(top_n)
        return list(query)
