from functools import wraps
from flask import session, redirect, request, flash, url_for
from .db import *


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not check_admin():
            flash('You are not an admin', category='error')
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not check_logged_in():
            flash('You are not logged in', category='error')
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