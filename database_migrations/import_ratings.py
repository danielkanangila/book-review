import settings
import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("./average_ratings.csv")
    reader = csv.reader(f)
    for isbn, average_rating in reader:
        rating = 0
        try:
            rating = float(average_rating) if average_rating else 0
        except ValueError:
            print(average_rating)
        db.execute(
            "INSERT INTO average_ratings (isbn, rating) VALUES (:isbn, :rating)",
            {"isbn": isbn, "rating": rating})
        print(f"Book with ISBN {isbn} and with rating {rating} has been added.")
        db.commit()


if __name__ == "__main__":
    main()
