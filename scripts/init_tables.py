import database
from database import db
from database import User
from database import Message


db.connect()
db.create_tables([User, Message])
db.close()
