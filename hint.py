from peewee import *
from .config import Config

db = SqliteDatabase(Config.DATABASE_URI)

class Hint(Model):
    key = CharField(index=True, unique=True)
    query = CharField()


    class Meta:
        database = db