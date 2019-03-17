import json


class User(object):
    """A discord user as described here:
    https://discordapp.com/developers/docs/resources/user#user-object

    Args:
        id: The user's id
        username: The user's username, not unique across the platform
        discriminator: The user's 4-digit discord-tag
        avatar: The user's avatar hash
    """

    def __init__(self, id, username, discriminator, avatar):
        self.id       = id
        self.username = username
        self.discriminator  = discriminator
        self.avatar   = avatar
        self.composite_username = "%s#%s" % (username, discriminator)

    @staticmethod
    def from_json(json_data):
        """Creates a User from a json object by extracting relevant items.

        Args:
            json_data: A user encoded as a json object.

        Returns:
            A User.
        """
        return User(id            = json_data["id"],
                    username      = json_data["username"],
                    discriminator = json_data["discriminator"],
                    avatar        = json_data["avatar"])
