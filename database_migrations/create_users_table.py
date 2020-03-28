import os

from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Boolean
#engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
#meta = MetaData()


def create_users_table(meta):

    users = Table(
        'users', meta,
        Column('id', Integer, primary_key=True),
        Column('first_name', String),
        Column('last_name', String),
        Column('email', String),
        Column('password', String),
        Column('is_active', Boolean, default=False)
    )
