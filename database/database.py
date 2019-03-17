from database import Member
from database import Message
from database import Thanks
from database.base_model import db
from peewee import fn, JOIN, SQL


class Database(object):
    """An interface to the bot's database."""

    def add_member(self, member_id, username):
        """Adds a member to the database.

        Args:
            member_id: Unique discord id for that member.
            username: Membername and discriminator combination string.

        Returns:
            A member record.
        """
        member = Member.create(member_id=member_id, username=username)
        return member

    def member_exists(self, member_id):
        """Checks whether the chosen member is present in the database.

        Args:
            member_id: Unique discord id for that member.

        Returns:
            Whether there is a member with that id in the database.
        """
        query = Member.select().where(Member.member_id == member_id)
        return query.exists()

    def get_member(self, member_id):
        """Gets a member from the database.

        Args:
            member_id: Unique discord id for that member.

        Returns:
            A member record.
        """
        return Member.select().where(Member.member_id == member_id).first()

    def delete_member(self, member_id):
        """Deletes a member from the database.

        Args:
            member_id: Unique discord id for that member.

        Returns:
            Whether the member was succesfully deleted.
        """
        return Member.delete().where(Member.member_id == member_id).execute()

    def add_message(self, message):
        """Adds a message to the database.

        Args:
            message: A discord message.

        Returns:
            A message record.
        """
        message = Message.create(content    = message.content,
                                 channel_id = message.channel_id,
                                 member     = message.author_id,
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

    def get_messages_for_member(self, member_id):
        """Gets all messages for the chosen member.

        Args:
            member_id: Unique discord id for that member.

        Returns:
            A list of message records.
        """
        return list(Message.select().where(Message.member == member_id))

    def delete_message(self, message_id):
        """Deletes a message from the database.

        Args:
            message_id: The message's uid in the database.

        Returns:
            Whether the message was succesfully deleted.
        """
        return Message.delete().where(Message.id == message_id).execute()

    def get_top_members_per_message_count(self, top_n=9):
        """Gets the most active members sorted by number of messages posted.

        Args:
            top_n: The maximum number of members to return.

        Returns:
            A list of the top n most active members.
        """
        query = Member.select(Member, fn.Count(Message.id).alias('count')) \
                      .join(Message, JOIN.RIGHT_OUTER) \
                      .group_by(Member) \
                      .order_by(SQL('count').desc()) \
                      .limit(top_n)
        return list(query)

    def get_top_members_per_num_characters(self, top_n=20):
        """Gets the most active members sorted by the sum of the number of
        characters in the messages they posted.

        Args:
            top_n: The maximum number of members to return.

        Returns:
            A list of the top n most active members.
        """
        query = Member.select(Member, fn.SUM(fn.LENGTH(Message.content)).alias('length')) \
                      .join(Message, JOIN.RIGHT_OUTER) \
                      .group_by(Member) \
                      .order_by(SQL('length').desc()) \
                      .limit(top_n)
        return list(query)

    def get_message_count_over_period(self, period):
        """Gets the number of messages posted by date.

        Args:
            period: The period over which to count messages, can be "day" or "week".

        Returns:
            A list of objects containing a date and a count (number of messages posted that day) for every date
            where a message was posted on the channel.
        """
        if period == "week":
            query = Message.select(db.truncate_date("day", Message.date).alias("date"), fn.Count(Message.id)) \
                           .group_by(db.truncate_date("day", Message.date))
        elif period == "day":
            query = Message.select(Message.date.hour.alias("date"), fn.Count(Message.id)) \
                           .group_by(Message.date.hour)
        else:
            raise ValueError("Unknown period.")
        return list(query)

    def thank_member(self, thanks_recipient_id, thanks_giver_id):
        """Adds a thank you to the database.

        Args:
            thanks_recipient_id: The id of the member to be thanked.
            thanks_giver_id: The id of the member who's thankful.

        Returns:
            A thanks record.
        """
        thanks = Thanks.create(given_to=thanks_recipient_id, given_by=thanks_giver_id)
        return thanks
