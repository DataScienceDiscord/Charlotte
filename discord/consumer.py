import copy
import requests


class Consumer(object):
    ENDPOINT = "https://discordapp.com/api/"
    CREATE_MESSAGE_ROUTE = "channels/%s/messages"
    URL     = "https://github.com/DataScienceDiscord/Charlotte"
    NAME    = "Charlotte"
    VERSION = 0.1

    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": "Bot %s" % self.token,
            "User-Agent":    "%s (%s, %s)" % (Consumer.NAME, Consumer.URL, Consumer.VERSION),
            "Content-Type":  "application/json"
        }

    def create_message(self, message):
        headers = self.headers
        if message.attachment != None:
            headers = copy.deepcopy(self.headers)
            headers["Content-Type"] = "multipart/form-data"

        requests.post(Consumer.ENDPOINT + Consumer.CREATE_MESSAGE_ROUTE % message.channel_id,
                      headers = headers,
                      data    = message.to_json())
