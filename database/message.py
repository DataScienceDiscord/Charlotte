import datetime

from database import BaseModel
from database import User
from peewee import TextField, ForeignKeyField, DateTimeField


class Message(BaseModel):
    content    = TextField()
    channel_id = TextField()
    user = ForeignKeyField(User, backref="messages")
    date = DateTimeField(default=datetime.datetime.now)
