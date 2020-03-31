from flask import g, request, redirect, url_for
from functools import wraps
from flask_bcrypt import generate_password_hash, check_password_hash
from random import randint
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if hasattr(g, 'user') is False:
            print('attribute found.')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


class Auth:
    def hash_password(self, password):
        return generate_password_hash(password).decode('utf8')

    def check_password(self, user_password, input_password):
        return check_password_hash(user_password, input_password)

    def create_user(self, db, user):

        # has password
        user['password'] = self.hash_password(user['password'])

        # add user to the db
        try:
            result = db.execute("INSERT INTO users (first_name, last_name, email, password)"
                  " VALUES (:first_name, :last_name, :email, :password) RETURNING id", user)

            db.commit()
            user_id = result.first()[0]

            # generate verification token and insert in db
            token = self.insert_verification_token(db, user_id)

            if token['error']:
                raise Exception(token['error'])
            else:
                # store user in session
                g['user'] = token
                return {"error": None, "status": "success"}


        except IntegrityError:
            db.rollback()
            return {"error": f"That email address '{user['email']}' is already in use."}
        except Exception as e:
            db.rollback()
            return {"error": str(e)}
        finally:
            db.rollback()

    def insert_verification_token(self, db, user_id):
        try:
            token = self.generate_token()
            date = datetime.now()
            result = db.execute("INSERT INTO verification_tokens (token, user_id, created_at) "
                       "VALUES (:token, :user_id, :created_at)"
                       "RETURNING token",
                       {"token": token, "user_id": user_id, "created_at": date})
            db.commit()
            return {"user_id": user_id, "verification_token": result.first()[0], "error": None}
        except Exception as e:
            db.rollback()
            return {"error": str(e)}

    def generate_token(self):
        n = 5
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)