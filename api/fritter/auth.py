import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from fritter.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('POST'))
def register():
    """Registers users.

    =====  ==================
    Error  Meaning
    =====  ==================
    0      Success
    1      Email Missing
    2      Username Missing
    3      Password Missing
    =====  ==================

    :return: { 'success': error }
    :rtype: json / int
    """
    if request.method == 'POST':
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
            'SELECT id FROM user WHERE email = ?', (email, )
            ).fetchone() is not None:
            error = 4

        if error == 0:
            db.execute(
                'INSERT INTO user (username, password, email) VALUES (?, ?)',
                (username, generate_password_hash(password), email)
            )
            db.commit()

    return {'status': error}

@bp.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Username not found."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
