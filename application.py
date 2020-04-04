import settings
import os
import sys
import requests as api_fetch

from flask import Flask, session, jsonify, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from assets import setup_assets
from auth import Auth, login_required, is_login

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
    def show_book(book_id):
        return book_id

    @app.route("/books")
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

    return app
