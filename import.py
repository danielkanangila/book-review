import settings
import csv
import os
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

api_key = os.getenv("API_KEY")
api_url = "https://www.goodreads.com/book/review_counts.json"

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    books = []
    for isbn, title, author, year in reader:
        result = requests.get(api_url, params={
            "api_key": api_key,
            "isbns": isbn
        })
        average_rating = result.json()['books'][0]['average_rating'] if result else None
        # book = {
        #     "isbn": isbn,
        #     "title": title,
        #     "author": author,
        #     "year": year,
        #     "average_rating":
        # }
        # books.append(book)
        print(f"Book {title} found with average rating of {average_rating}")
        db.execute("INSERT INTO books (isbn, title, author, year, average_rating) VALUES (:isbn, :title, :author, :year, :average_rating)",
            {"isbn": isbn, "title": title, "author": author, "year": year, "average_rating": average_rating})
        print(f"Book {title} has been added to the database.")
        db.commit()

    #for isbn, title, author, year, average_rating in books:



if __name__ == "__main__":
    main()
