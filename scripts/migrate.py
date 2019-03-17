import peeweedbevolve
import database
from database import db
from database import Member
from database import Message

db.evolve()
# migrator = PostgresqlMigrator(db)


# Add thanks related fields to members
