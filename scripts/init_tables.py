import database
from database import db
from database import Member
from database import Message


db.connect()
db.create_tables([Member, Message])
db.close()
