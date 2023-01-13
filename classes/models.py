import os

from peewee import BigIntegerField, FloatField, Model, SqliteDatabase, TextField


DB = SqliteDatabase(os.path.join('data', 'users.db'))


class BaseModel(Model):
    class Meta:
        database = DB
        order_by = 'user_id'


class Settings(BaseModel):
    user_id = BigIntegerField(unique=True)
    low = FloatField()
    high = FloatField()


class History(BaseModel):
    user_id = BigIntegerField(unique=True)
    query_history = TextField()
