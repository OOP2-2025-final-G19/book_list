from peewee import Model, CharField, IntegerField,BooleanField
from .db import db


class Registration(Model):
    title = CharField()
    author = CharField()
    day = IntegerField()
    review = IntegerField()
    thoughts = CharField()
    is_read = BooleanField(default=False)

    class Meta:
        database = db
