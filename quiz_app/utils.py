from flask import session, redirect, request, flash, url_for
from .db import *

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
 

def check_logged_in():
    if session.get('logged_in'):
        flash('You are already logged in', category='error')
        return redirect(url_for('home'))
    else:
        return redirect('/users.login?continue_to=' + request.url)