from playhouse.postgres_ext import *
import database.config

db = PostgresqlExtDatabase(database.config.NAME,
                           user     = database.config.USER,
                           password = database.config.PASSWORD,
                           port     = database.config.PORT)

class BaseModel(Model):
    class Meta:
        database = db
