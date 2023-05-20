from flask import session, redirect, request
from .db import db_query_single

def get_user_id():
    if session['logged_in']:
        return session['logged_in']
    return None
 

def get_user():
    user_id = get_user_id()
    if user_id == None:
        return None
    return db_query_single("SELECT * FROM users WHERE id=%s", [ user_id ])
 

def check_logged_in():
    if not get_user_id():
        return redirect('/login?continue_to=' + request.url)
    return None