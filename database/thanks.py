import datetime

from database import BaseModel
from database import Member
from peewee import ForeignKeyField, DateTimeField


class Thanks(BaseModel):
    given_by = ForeignKeyField(Member, backref='thanks_given')
    given_to = ForeignKeyField(Member, backref='thanks_received')
    date     = DateTimeField(default=datetime.datetime.now)
