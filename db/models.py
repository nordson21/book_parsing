from peewee import *
db = SqliteDatabase('db/books.db')


class BaseModel(Model):
    class Meta:
        database = db


class Book(BaseModel):
    book_id = IntegerField(primary_key=True, unique=True)
    name = CharField()
    author = CharField()
    description = CharField()
    image_url = CharField()
    download_url = CharField()

    class Meta:
        database = db


class LastSent(BaseModel):
    book_id = IntegerField(primary_key=True, unique=True)


db.create_tables([Book, LastSent])
