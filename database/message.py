import datetime

from database import BaseModel
from database import Member
from peewee import TextField, ForeignKeyField, DateTimeField


class Message(BaseModel):
    content    = TextField()
    channel_id = TextField()
    member = ForeignKeyField(Member, backref="messages")
    date = DateTimeField(default=datetime.datetime.now)
