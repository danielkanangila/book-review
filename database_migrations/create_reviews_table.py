import os

from sqlalchemy import create_engine, MetaData, Table, Column, String, Date, Integer, Boolean, ForeignKey, Text


def create_reviews_table(meta):

    reviews = Table(
        'reviews', meta,
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('book_id', Integer, ForeignKey('books.id')),
        Column('comment', Text),
        Column('rating', Integer),
        Column('created_at', Date),
        Column('updated_at', Date)
    )