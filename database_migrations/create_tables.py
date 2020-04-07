create_books_table = """
DROP TABLE IF EXISTS books;

CREATE TABLE books (
    id  SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year VARCHAR NOT NULL
)
"""

create_average_ratings_table = """
DROP TABLE IF EXISTS average_ratings;

CREATE TABLE average_ratings (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    rating FLOAT
)      
"""

create_users_table = """
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password text NOT NULL,
    is_active BOOLEAN DEFAULT NULL,
    access_token BOOLEAN DEFAULT NULL
)
"""

create_reviews_table = """
DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY ,
    user_id INTEGER NOT NULL ,
    book_id INTEGER NOT NULL ,
    comment VARCHAR NOT NULL ,
    rating INTEGER DEFAULT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT "reviews_book_id_fkey" FOREIGN KEY (book_id) REFERENCES books(id) NOT DEFERRABLE,
    CONSTRAINT "reviews_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE
)
"""

create_table_verification_tokens = """
DROP TABLE IF EXISTS verification_tokens;

CREATE TABLE verification_tokens (
    id SERIAL PRIMARY KEY ,
    user_id INTEGER NOT NULL ,
    token text UNIQUE NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp DEFAULT NULL,
    CONSTRAINT "verification_tokens_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE
)
"""

create_tables = [
    {"name": "books", "sql": create_books_table},
    {"name": "average_ratings", "sql": create_average_ratings_table},
    {"name": "users", "sql": create_users_table},
    {"name": "reviews", "sql": create_reviews_table},
    {"name": "verification_tokens", "sql": create_table_verification_tokens}
]
