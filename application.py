import settings
import os
import sys
import operator
import requests as api_fetch
import datetime

from flask import Flask, session, jsonify, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from assets import setup_assets
from auth import Auth, login_required, is_login
from utils import format_reviews_data

from flask_jwt_extended import (
    JWTManager,
    get_raw_jwt
)


def create_app():

    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ['access']
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    jwt = JWTManager(app)

    # Check for environment variable
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")

    # Configure session to use filesystem
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Storage engine to save revoked token
    blacklist = set()

    # check if token exist in blacklist
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    # Set up assets
    # setup_assets(app)

    # Set up database
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))

    # get API key
    API_KEY = os.getenv("API_KEY")
    API_URL = "https://www.goodreads.com/book/review_counts.json"

    # User authentication class instance
    auth = Auth()

    # Home route (book list)
    @app.route("/")
    @login_required
    def index():
        row_count = db.execute("SELECT COUNT(*) FROM books").first()[0]
        limit = 50
        current_page_n = 1 if not request.args.get('page') else request.args.get('page')
        offset = (current_page_n-1) * limit
        result = db.execute(f"SELECT * FROM books ORDER BY id LIMIT {limit} OFFSET {offset}").fetchall()

        return render_template('index.html', data={
            "result": result,
            "row_count": row_count,
            "offset": offset
        })

    @app.route("/book/<int:book_id>")
    @login_required
    def show_book(book_id):
        book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
        reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id ORDER BY id DESC ",
                             {"book_id": book['id']}).fetchall()

        api_res = api_fetch.get(API_URL, params={
            "key": API_KEY,
            "isbns": book['isbn']
        })
        if not api_res:
            formatted_data = {}
        else:
            formatted_data = format_reviews_data(api_res.json()['books'][0])

        return render_template('book.html', book=book, reviews=reviews, good_read_data=formatted_data)

    # store review
    @app.route("/book/<int:book_id>", methods=["POST"])
    @login_required
    def store_review(book_id):
        # check user has already reviews the book
        reviews = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
                             {"user_id": session['user_id'], "book_id": book_id}).fetchone()

        if reviews:
            return {
                "error": "You are already reviewed this book."
            }, 500

        # check that comment is not empty
        comment = request.json.get('comment')
        if not comment:
            return {
                "error": "Comment is required"
            }, 500

        data = {
            "user_id": session['user_id'],
            "book_id": book_id,
            "comment": comment,
            "rating": request.json.get('rating'),
            "created_at": datetime.datetime.now(),
        }

        result = db.execute("INSERT INTO reviews (user_id, book_id, comment, rating, created_at)"
                            "VALUES (:user_id, :book_id, :comment, :rating, :created_at)"
                            "RETURNING comment, rating, created_at",
                            data)
        db.commit()

        return jsonify({"result": [dict(row) for row in result]}), 200

    # return data for pagination
    @app.route("/books")
    @login_required
    def books_as_json():
        row_count = db.execute("SELECT COUNT(*) FROM books").first()[0]
        limit = 50
        total_page = int(row_count / limit)
        current_page_n = 1 if not request.args.get('page') else int(request.args.get('page'))
        next_page_n = current_page_n + 1
        previous_page_n = current_page_n - 1
        offset = (current_page_n - 1) * limit
        result = db.execute(f"SELECT * FROM books ORDER BY id LIMIT {limit} OFFSET {offset}").fetchall()

        return jsonify({
            "result": [dict(row) for row in result],
            "previous_page": f"?page={previous_page_n}" if previous_page_n > -1 else "",
            "next_page": f"?page={next_page_n}" if current_page_n <= total_page else "",
            "row_count": row_count,
            "offset": offset
        })

    @app.route("/logout", methods=['GET'])
    @login_required
    def logout():
        session['access_token'] = None;
        return redirect(url_for('login'))

    @app.route("/login", methods=["GET", "POST"])
    @is_login
    def login():
        if request.method == "GET":
            return render_template('auth/login.html')
        if request.method == "POST":
            email = request.json.get('email', None)
            password = request.json.get('password', None)
            token = auth.authenticate(db, email=email, password=password)
            return jsonify(token), 200 if not token['error'] else 404

    @app.route("/signup", methods=["GET", "POST"])
    @is_login
    def signup():
        if request.method == "GET":
            return render_template('auth/signup.html')
        elif request.method == "POST":
            new_user = request.get_json()
            result = auth.create_user(db, new_user)

            return jsonify(result), 200 if not result['error'] else 500

    # to be update for full working, does not involve in current registration process
    @app.route("/reset-password", methods=["GET", "POST"])
    def reset_password():
        if request.method == "GET":
            return render_template('auth/reset-password.html')

    @app.route("/email-verification", methods=["GET", "POST"])
    def verify_email():
        if request.method == "GET":
            return render_template('auth/email-verification.html')

    @app.route("/update-db")
    def update_db():
        result = db.execute('SELECT * FROM books').fetchall()
        return jsonify([dict(row) for row in result])
    # API Access
    @app.route('/api/<string:isbn>')
    def get_reviews(isbn):
        book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()

        review_count = db.execute("SELECT COUNT(*) FROM reviews WHERE book_id = :book_id",
                                  {"book_id": book['id']}).first()[0]
        average_score = db.execute("SELECT AVG(rating) FROM reviews WHERE book_id = :book_id",
                                   {"book_id": book['id']}).first()[0]
        data = {
            "title": book['title'],
            "author": book['author'],
            "year": book['year'],
            "isbn": book['isbn'],
            "review_count": review_count if review_count else 0,
            "average_score": f"{average_score:.1f}" if average_score else 0,
        }

        return jsonify(data), 200

    return app
