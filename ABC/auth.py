import functools
import re 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response
)
from werkzeug.security import check_password_hash, generate_password_hash

from ABC.db import get_db

bp = Blueprint('auth', __name__)

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
#-------------------------------------------VISTAS--------------------------------------
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if g.user is None:
        if request.method == 'POST':

            email = request.form['Username']
            password = request.form['Password']
            db = get_db()
            error = None
            if not valid_email(email):
                error = 'Please enter a valid email.'
            elif not email:
                error = 'Email is required.'
            elif not password:
                error = 'Password is required.'
            elif db.execute(
                'SELECT id FROM user WHERE Username = ?', (email,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(email)

            if error is None:
                db.execute(
                    'INSERT INTO user (Username, Password) VALUES (?, ?)',
                    (email, generate_password_hash(password))
                )
                db.commit()
                return redirect(url_for('auth.login'))

            #guarda mensajes que se pueden recuperar cuando se renderice el template (html)
            flash(error)

        return render_template('auth/register.html')
    else:
        return redirect(url_for('evento.index')) 

@bp.route('/', methods=('GET', 'POST'))
def login():
    if g.user is None:
        if request.method == 'POST':
            email = request.form['Username']
            password = request.form['Password']
            db = get_db()
            error = None
            user = db.execute(
                'SELECT * FROM user WHERE Username = ?', (email,)
            ).fetchone()

            if email is None:
                error = 'Incorrect email.'
            elif not valid_email(email):
                error = 'Please enter a valid email.'
            elif not check_password_hash(user['Password'], password):
                error = 'Incorrect password.'

            if error is None:

                session.clear()
                session['user_id'] = user['id']
                resp=make_response(redirect(url_for('evento.index')))
                resp.headers['id']=session['user_id']
                return resp

            flash(error)

        return render_template('auth/login.html')
    else:
        resp=make_response(redirect(url_for('evento.index')))
        resp.headers['id']=session['user_id']
        return resp
        
#Se ejecuta antes de cualquier request
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
    return redirect(url_for('auth.login'))

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def valid_email(email):
    if(re.search(regex,email)):  
        return True
    else:  
        return False