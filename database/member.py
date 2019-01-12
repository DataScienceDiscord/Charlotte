from database import BaseModel
from peewee import TextField


class Member(BaseModel):
    member_id  = TextField(primary_key=True)
    username = TextField()
