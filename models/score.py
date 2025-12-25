from peewee import Model, ForeignKeyField, IntegerField
from .db import db
from .user import User
from .subject import Subject

class Score(Model):
    user = ForeignKeyField(User, backref='scores')
    subject = ForeignKeyField(Subject, backref='scores')
    value = IntegerField()
    month = IntegerField()

    class Meta:
        database = db
