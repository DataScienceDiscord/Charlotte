import database
from database import db
from database import Member
from database import Message
from database import Thanks


db.connect()
db.create_tables([Member, Message, Thanks])
db.close()
