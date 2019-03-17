import copy
import requests


class Consumer(object):
    """An interface for discord's REST api as described here:
    https://discordapp.com/developers/docs/reference

    Args:
        token: The bot token.
    """
    ENDPOINT = "https://discordapp.com/api/"
    CREATE_MESSAGE_ROUTE = "channels/%s/messages"
    LIST_GUILD_MEMBERS_ROUTE = "guilds/%s/members"
    LIST_GUILD_INVITES_ROUTE = "guilds/%s/invites"
    URL     = "https://github.com/DataScienceDiscord/Charlotte"
    NAME    = "Charlotte"
    VERSION = 0.1

    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": "Bot %s" % self.token,
            "User-Agent":    "%s (%s, %s)" % (Consumer.NAME, Consumer.URL, Consumer.VERSION)
        }

    def create_message(self, message):
        """Posts a message to the CREATE_MESSAGE route.

        Args:
            message: The Message to be sent.
        """
        route   = Consumer.ENDPOINT + Consumer.CREATE_MESSAGE_ROUTE % message.channel_id

        if message.attachment != None:
            files = {"file": message.attachment}
            data  = {"payload_json": message.to_json()}
            result = requests.post(route, headers=self.headers, data=data, files=files)
        else:
            result = requests.post(route, headers=self.headers, json=message.to_payload())

    def list_guild_members(self, guild_id, limit=1000):
        """Gets a list of the guild members.

        Args:
            guild_id: The guild whose members we want.
            limit: The number of members to get.
        """
        headers = copy.deepcopy(self.headers)
        params  = {"limit": limit}
        return requests.get(Consumer.ENDPOINT + Consumer.LIST_GUILD_MEMBERS_ROUTE % guild_id,
                            headers = headers,
                            params  = params)

    def list_guild_invites(self, guild_id):
        """Gets a list of the active guild invites.

        Args:
            guild_id: The guild whose invites we want.
        """
        headers = copy.deepcopy(self.headers)
        return requests.get(Consumer.ENDPOINT + Consumer.LIST_GUILD_INVITES_ROUTE % guild_id,
                            headers = headers)
