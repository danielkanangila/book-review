import os
import requests

from flask import Flask, session, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# get API key
API_KEY = os.getenv("API_KEY")
API_URL = "https://www.goodreads.com/book/review_counts.json"


@app.route("/")
def index():
    res = requests.get(API_URL, params={"key": API_KEY, "isbns": "0380795272"})
    return jsonify(res.json())
