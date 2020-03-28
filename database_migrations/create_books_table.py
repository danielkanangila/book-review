import os

from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
#engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
#meta = MetaData()


def create_books_table(meta):
    books = Table(
        'books', meta,
        Column('id', Integer, primary_key=True),
        Column('isbn', String),
        Column('title', String),
        Column('author', String),
        Column('year', String)
    )
