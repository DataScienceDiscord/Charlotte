import json
import datetime


class Invite(object):
    """A discord invite as described here:
    https://discordapp.com/developers/docs/resources/invite#invite-object

    Args:
        content: The contents of the message.
        channel_id: The id of the channel the message will be written to.
        author_id: The unique id of the user who sent/sends the message.
        username: The current username#discriminator combo for that user.
        timestamp: The time of the message.
        attachment: The file that will be attached to the message.
    """

    def __init__(self, code, guild_id, channel, created_at, temporary, uses, max_uses, max_age, inviter_id):
        self.code       = code
        self.guild_id   = guild_id
        self.channel    = channel
        self.created_at = created_at
        self.temporary  = temporary
        self.uses       = uses
        self.max_uses   = max_uses
        self.max_age    = max_age
        self.inviter_id = inviter_id

    @staticmethod
    def from_json(json_data):
        """Creates an Invite from a json object by extracting relevant items.

        Args:
            json_data: An invite item encoded as a json object.

        Returns:
            An Invite.
        """
        created_at = datetime.datetime.strptime(json_data["created_at"][:-6], "%Y-%m-%dT%H:%M:%S.%f")
        return Invite(code       = json_data["code"],
                      guild_id   = json_data["guild"]["id"],
                      channel    = json_data["channel"]["id"],
                      created_at = created_at,
                      temporary  = json_data["temporary"],
                      uses       = json_data["uses"],
                      max_uses   = json_data["max_uses"],
                      max_age    = json_data["max_age"],
                      inviter_id = json_data["inviter"]["id"])
