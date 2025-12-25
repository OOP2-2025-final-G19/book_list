from peewee import Model, ForeignKeyField, IntegerField
from .db import db
from .user import User
from .subject import Subject

class Score(Model):
    user = CharField()
    author = CharField()
    day = IntegerField()
    month = IntegerField()

    class Meta:
        database = db
