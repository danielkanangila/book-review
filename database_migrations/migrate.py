# import os
#
# from sqlalchemy import create_engine, MetaData
#
# from create_users_table import create_users_table
# from create_books_table import create_books_table
# from create_reviews_table import create_reviews_table
#
#
# def main():
#     engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
#     meta = MetaData()
#     create_books_table(meta)
#     create_users_table(meta)
#     create_reviews_table(meta)
#     meta.create_all(engine)
#
#
# if __name__ == "__main__":
#     main()
import csv
import os
import sys
import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from create_tables import create_tables

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    for table in create_tables:
        db.execute(table['sql'])
        print(f"table {table['name']} has been created.")
        db.commit()


if __name__ == "__main__":
    main()
