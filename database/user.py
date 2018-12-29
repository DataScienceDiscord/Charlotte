from database import BaseModel
from peewee import TextField


class User(BaseModel):
    user_id  = TextField(primary_key=True)
    username = TextField()
