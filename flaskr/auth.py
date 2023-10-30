import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for 
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db


#creating blueprint named 'auth'
# __name__ tells blueprint where it's defined
bp = Blueprint('auth', __name__, url_prefix='/auth')

#has views to register new users and to login/out

#associating URL /register with register view function below
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try: 
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?,?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth_login"))
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:

            # session is a dictionary that stores data across requests
                # data is stored in a cookie and allows subsequent requests without validation of user
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)
    return render_template('auth/login.html')


# registers func that runs before view func, no matter the URL requested
# checks db for user_id in session, then grabs that data fpr storage in g.user
@bp.before_app_request
def load_logged_in_user():
    user_id - session.get('user_id')

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


# Checking Auth in Every View Func is applied to
# this decorator will returns a new function wrapping whichever view its applied to
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view