from flask import jsonify


class Books:
    def __init__(self, db):
        self.db = db
        self.select_query = """
            SELECT books.id, books.isbn, books.title, books.author, books.year,
            average_ratings.rating as average_rating
            from books left join average_ratings on books.isbn = average_ratings.isbn
        """

    def count(self):
        return self.db.execute('select count(*) from books').first()[0]

    def fetchall(self, query):
        q = f"{self.select_query} {query}"
        result = self.db.execute(q).fetchall()
        return result if not result else [dict(row) for row in result]

    def search(self, q):
        return self.fetchall(query=f"where books.title like '%{q}%' or books.author like '%{q}%' or books.isbn like '%{q}%'")

    def fetchone(self, query, value):
        q = f"{self.select_query} {query}"
        return self.db.execute(q, value).fetchone()

    def paginate(self, request):
        row_count = self.count()
        limit = 50
        total_page = int(row_count / limit)
        current_page_n = 1 if not request.args.get('page') else int(request.args.get('page'))
        next_page_n = current_page_n + 1
        previous_page_n = current_page_n - 1
        offset = (current_page_n - 1) * limit
        result = self.fetchall(query=f"LIMIT {limit} OFFSET {offset}")

        return jsonify({
            "result": [dict(row) for row in result],
            "previous_page": f"?page={previous_page_n}" if previous_page_n > -1 else "",
            "next_page": f"?page={next_page_n}" if current_page_n <= total_page else "",
            "row_count": row_count,
            "offset": offset
        })

    def join_reviews(self, isbn):
        q = """
            select books.title, books.author, books.year,
            books.isbn, count(reviews.*) as review_count, 
            to_char(avg(reviews.rating), 'FM999999999.00') as average_rating 
            from books left join reviews on book_id = books.id where
            books.isbn = :isbn
            group by books.title, books.author, books.year, 
            books.isbn
        """
        result = self.db.execute(q, {"isbn": isbn}).fetchall()
        return [dict(row) for row in result]
