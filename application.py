import os
import requests

from flask import Flask, session, jsonify, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from assets import setup_assets


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
    setup_assets(app)

    # Set up database
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))

    # get API key
    API_KEY = os.getenv("API_KEY")
    API_URL = "https://www.goodreads.com/book/review_counts.json"

    @app.route("/")
    def index():
        return render_template('index.html')

    return app
