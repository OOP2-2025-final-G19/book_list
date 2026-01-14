from peewee import Model, CharField, IntegerField,BooleanField, DateTimeField
from .db import db


class Registration(Model):
    title = CharField() #書籍のタイトル用　文字列型
    author = CharField() #書籍の著者用　文字列型
    day = DateTimeField() #書籍を登録した日用　データ(日付)型
    review = IntegerField() #書籍を評価用　整数型
    thoughts = CharField() #書籍の感想用　文字列型
    is_read = BooleanField(default=False) #書籍の読書状況用　真偽型
    image_path = CharField(null=True)
    class Meta:
        database = db
