import os
import sys
import requests as api_fetch

from flask import Flask, session, jsonify, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from assets import setup_assets
from auth import Auth, login_required


def create_app():

    app = Flask(__name__)

    # Check for environment variable
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")

    # Configure session to use filesystem
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

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

    @app.route("/")
    @login_required
    def index():
        return render_template('index.html')

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template('auth/login.html')

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "GET":
            return render_template('auth/signup.html')
        elif request.method == "POST":
            new_user = request.get_json()
            result = auth.create_user(db, new_user)
            if result['error']:
                return result, 500
            else:
                return {"status": "success"}, 200

    @app.route("/reset-password", methods=["GET", "POST"])
    def rest_password():
        if request.method == "GET":
            return render_template('auth/reset-password.html')

    @app.route("/email-verification", methods=["GET", "POST"])
    def verify_email():
        if request.method == "GET":
            return render_template('auth/email-verification.html')

    return app
