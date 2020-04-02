from flask import g, request, redirect, url_for, session
from functools import wraps
from flask_bcrypt import generate_password_hash, check_password_hash
from random import randint
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    create_access_token,
    verify_jwt_in_request,
    get_jwt_identity
)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session.get('access_token', None)
        if not access_token:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def is_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session.get('access_token', None)
        if access_token:
            return redirect(url_for('index'))
        return f(*args, **kwargs)

    return decorated_function


class Auth:

    def hash_password(self, password):
        return generate_password_hash(password).decode('utf8')

    def check_password(self, user_password, input_password):
        return check_password_hash(user_password, input_password)

    def authenticate(self, db, email, password):
        user = db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).fetchone()
        if not user:
            return {'error': f'User {email} does not exist.'}
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user['email'])
            session['access_token'] = access_token
            session['user_id'] = user['id']
            return {
                'error': False,
                'access_token': access_token
            }
        else:
            return {
                'error': 'Bad credentials.'
            }

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
                access_token = create_access_token(identity=user['email'])
                session['access_token'] = access_token
                session['user_id'] = user_id
                # return token
                return {
                    "error": None,
                    "status": "success",
                    'access_token': access_token
                }

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

