from functools import wraps
from flask import session, redirect, request, flash, url_for
from .db import *


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in
        if 'id' not in session:
            # User is not logged in, redirect to login page
            flash('You must be logged in to access this page', category='error')
            return redirect(url_for('users.login'))

        # User is logged in, execute the wrapped function
        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in
        if not check_admin():
            flash('You must be admin to access this page', category='error')
            return redirect(url_for('home'))

        # User is logged in, execute the wrapped function
        return f(*args, **kwargs)

    return decorated_function

def get_user_id():
    if session.get('id'):
        return session['id']
    return None

 

def get_user():
    user_id = get_user_id()
    if user_id == None:
        return None
    return db_query_single("SELECT * FROM user WHERE id=%s", [ user_id ])

def get_user_by_id(id):
    return db_query_single("SELECT * FROM user WHERE id=%s", [ id ])
 
def check_admin():
    if session.get('id'):
        user = get_user_by_id(session.get('id'))
        if user.get('is_admin'):
            return True
    return False

def check_logged_in():
    if session.get('logged_in'):
        flash('You are already logged in', category='error')
        return redirect(url_for('home'))
    else:
        return redirect('/users.login?continue_to=' + request.url)