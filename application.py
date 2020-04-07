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
from utils import format_reviews_data, validate_reviews

from flask_jwt_extended import (
    JWTManager,
    get_raw_jwt
)

from models.books import Books
from models.reviews import Reviews

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

    # models
    books = Books(db)
    reviews = Reviews(db)

    # Home route (book list)
    @app.route("/")
    @login_required
    def index():
        return render_template('index.html')

    # Book list page
    @app.route("/library")
    @login_required
    def library():
        return render_template('library.html', data={
            "result": books.fetchall(query="ORDER BY id LIMIT 50"),
            "row_count": books.count()
        })

    # search endpoint
    @app.route("/book/search")
    @login_required
    def search():
        return jsonify({
            "result": books.search(request.args.get('q'))
        }), 200

    @app.route("/book/<int:book_id>")
    @login_required
    def show_book(book_id):
        book = books.fetchone(query="where books.id = :id", value={"id": book_id})
        api_res = api_fetch.get(API_URL, params={"key": API_KEY, "isbns": book['isbn']})
        formatted_data = format_reviews_data(api_res) if api_res else {}

        return render_template(
            'book.html',
            book=book,
            reviews=reviews.fetchall(query="where book_id = :book_id  ORDER BY id DESC", value={"book_id": book['id']}),
            good_read_data=formatted_data
        )

    # store review
    @app.route("/book/<int:book_id>", methods=["POST"])
    @login_required
    def store_review(book_id):
        validated = validate_reviews(reviews, book_id, request, session)
        if validated is True:
            review = reviews.insert({
                "user_id": session['user_id'],
                "book_id": book_id,
                "comment": request.json.get('comment'),
                "rating": request.json.get('rating')
            })
            return jsonify({"result": review}), 200
        else:
            return validated, 500

    # return data for pagination
    @app.route("/books")
    @login_required
    def books_as_json():
        return books.paginate(request), 200

    # API Access
    @app.route('/api/<string:isbn>')
    def get_reviews(isbn):
        return jsonify(books.join_reviews(isbn)), 200

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

    return app
