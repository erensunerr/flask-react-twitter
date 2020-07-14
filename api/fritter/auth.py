import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

from werkzeug.security import check_password_hash, generate_password_hash

import jwt, datetime

from fritter.db import get_db

def encode_auth_token(user_id):
    """Generates the auth token. MAKE SURE THE OUTPUT IS NON-NEGATIVE.

    :param user_id: id of the user in database
    :type user_id: str / int
    :return: The token
    :rtype: str

    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, minutes=0, seconds=0), #expiry date of the token
            'iat': datetime.datetime.utcnow(), #time token is generated
            'sub': user_id # subject of the token
        }

        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        ).hex()
    except Exception as e:
        return -1

def decode_auth_token(token):
    """Decodes the generated auth token. MAKE SURE THE OUTPUT IS NON-NEGATIVE

    :param token: Token
    :type token: str
    :return: user_id
    :rtype: str

    """
    try:
        payload = jwt.decode(bytes.fromhex(token), current_app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return -1
    except jwt.InvalidTokenError:
        return -2




bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register(): # TODO: code the input checks
    """Registers users.

    =====   ==================
    Error   Meaning
    =====   ==================
    0       Success
    1       Email Missing
    2       Username Missing
    3       Password Missing
    4       Pre-existing user
    =====   ==================

    :param post username:
    :param post email:
    :param post password:
    :return: { 'status': error }
    :rtype: json / int
    """
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    db = get_db()
    error = 0
    if not email:
        error = 1
    elif not username:
        error = 2
    elif not password:
        error = 3
    elif db.execute(
        'SELECT id FROM users WHERE email = ?', (email, )
        ).fetchone() is not None:
        error = 4

    if error == 0:
        db.execute(
            'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
            (username, generate_password_hash(password), email)
        )
        db.commit()

    return {'status': error}


@bp.route("/login", methods=['POST'])
def login():
    """Gives a token given password and email.

    :param post email:
    :param post password:

    =====   ===================
    Error   Meaning
    =====   ===================
    0       Success
    1       Email not found
    2       Incorrect password
    =====   ===================

    :return: {'status': int(error), 'token': user token}
    """
    email = request.form['email']
    password = request.form['password']
    db = get_db()
    error = 0
    user = db.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()

    if user is None:
        error = 1
    elif not check_password_hash(user['password'], password):
        error = 2

    if error == 0:
        return {'status': 0, 'token': encode_auth_token(user['id'])}

    return {'status': error}


def login_required(view):
    """Decorator for authorized functions.

    :param post token: Auth token provided by login
    :param view: a function.
    :type view: function
    :return: modified function
    :rtype: function

    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        token = request.form['token']
        user_id = decode_auth_token(request.form['token'])
        if user_id < 0:
            return {'status': -1}
        else:
            g.user = get_db().execute(
                'SELECT * FROM users WHERE id = ?', (user_id,)
            ).fetchone()
            return view(**kwargs)
    return wrapped_view
# IDEA: add password recovery
