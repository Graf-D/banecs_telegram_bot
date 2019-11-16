from peewee import SqliteDatabase, Model, TextField, IntegerField

from banecbot.model import Anecdote, db
from banecbot.db_creation.posts_fetcher import fetch_posts


def main():
    db.create_tables([Anecdote])
    
    for post in fetch_posts():
        anecdote = Anecdote.create(text=post.text, likes=post.likes)
        anecdote.save()
    
    db.close()


if __name__ == '__main__':
    main()
