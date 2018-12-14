import json


class Message(object):

    def __init__(self, content, channel_id, user, username, timestamp=None, attachment=None):
        self.content    = content
        self.channel_id = channel_id
        self.user       = user
        self.username   = username
        self.attachment = attachment

    @staticmethod
    def from_payload(payload):
        data = payload.data
        return Message(content    = data["content"],
                       channel_id = data["channel_id"],
                       user       = data["author"]["id"],
                       username   = data["author"]["username"] + "#" + data["author"]["discriminator"],
                       timestamp  = data["timestamp"])

    def to_json(self):
        payload =  {
            "content": self.content,
            "tts": False,
            "file": self.attachment,
            "embed": None,
            "payload_json": None
        }
        return json.dumps(payload)
