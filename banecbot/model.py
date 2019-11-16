from peewee import SqliteDatabase, Model, TextField, IntegerField


db = SqliteDatabase('anecdotes.db')


class Anecdote(Model):
    text = TextField()
    likes = IntegerField()

    class Meta:
        database = db
