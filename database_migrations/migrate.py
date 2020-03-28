import os

from sqlalchemy import create_engine, MetaData

from create_users_table import create_users_table
from create_books_table import create_books_table
from create_reviews_table import create_reviews_table


def main():
    engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
    meta = MetaData()
    create_books_table(meta)
    create_users_table(meta)
    create_reviews_table(meta)
    meta.create_all(engine)


if __name__ == "__main__":
    main()