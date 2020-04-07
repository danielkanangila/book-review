import datetime


class Reviews:
    def __init__(self, db):
        self.db = db
        self.table_name = 'reviews'
        self.select_query = f"""
            select * from {self.table_name}
        """

    def fetchall(self, query, value):
        q = f"{self.select_query} {query}"
        result = self.db.execute(q, value).fetchall()
        return result if not result else [dict(row) for row in result]

    def fetchone(self, query, value):
        q = f"{self.select_query} {query}"
        result = self.db.execute(q, value).fetchone()
        return result

    def insert(self, data):
        q = """
            INSERT INTO reviews (user_id, book_id, comment, rating, created_at)
            VALUES (:user_id, :book_id, :comment, :rating, :created_at)
            RETURNING comment, rating, created_at
        """
        data["created_at"] = datetime.datetime.now()
        result = self.db.execute(q, data)
        self.db.commit()

        return result if not result else [dict(row) for row in result]
