from flask import Blueprint, session, render_template, redirect, url_for, request, flash

users = Blueprint('users', __name__, url_prefix='/users')

from ..forms import *

from ..quiz_register import *
from ..admin_register import *
from ..answer_register import *
from ..user_register import *
from ..user_has_quiz import *
from ..user_has_answer import *
from ..mysql_cursor import *
from ..db import *
from ..utils import *

import random
from datetime import datetime
from datetime import timedelta


import werkzeug
import random

@users.route('/', methods=['POST', 'GET'])
def home():
    if not session.get('logged_in'):
        flash('You are not logged in', category='error')
        return redirect(url_for('login'))
    else:
        quizes = db_query_rows("SELECT * FROM quiz")
        return render_template('user_dashboard.html', quizes=quizes)


@users.route('/register', methods=["GET", "POST"])
def register():
    if session.get('logged_in'):
        flash('You are already logged in', category='error')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        is_admin = form.is_admin.data
        username = form.username.data
        email = form.email.data
        password_hash = werkzeug.security.generate_password_hash(form.password.data)
        if is_admin:
            first_name = form.first_name.data
            last_name = form.last_name.data
            db_exec('''INSERT INTO user (is_admin, username, email, password_hash, first_name, last_name) 
            VALUES (%s, %s, %s, %s, %s, %s)''', 
            (is_admin, username, email, password_hash, first_name, last_name))

            flash(f'Successfully created admin {username}', category='success')
        else:
            db_exec('''INSERT INTO user (is_admin, username, email, password_hash) 
            VALUES (%s, %s, %s, %s)''', 
            (is_admin, username, email, password_hash))

            flash(f'Successfully created user {username}', category='success')

        return redirect(url_for('login'))
        
    return render_template('register.html', form=form)



@users.route('/logout', methods=["GET", "POST"])
def logout():
    if session.get('logged_in'):
        username = session.pop('username')
        session.clear() # clear the rest
        flash(f'logged out as {username}', 'info')
        return redirect(url_for('home'))
    else:
        flash('not logged in', 'info')
        return redirect(url_for('login'))




@users.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            usr = db_query_single("SELECT * FROM user WHERE username=%s", [username])
            if usr:
                user_id, is_admin, username, email, password_hash, first_name, last_name, created_at = usr
                if werkzeug.security.check_password_hash(password_hash, password):
                    session['id'] = user_id
                    session['is_admin'] = is_admin
                    session['username'] = username
                    session['email'] = email
                    session['password_hash'] = password_hash
                    session['first_name'] = first_name
                    session['last_name'] = last_name
                    session['created_at'] = created_at
                    session['logged_in'] = True
                    if is_admin:
                        flash(f'Successfully logged in as admin {username}', category='success')
                    else:
                        flash(f'Successfully logged in as user {username}', category='success')
                    return redirect(url_for('user_dashboard', username=username))
                else:
                    flash('Incorrect password', category='error')
                    return redirect(url_for('login'))
            else:
                flash(f'user does not exist {username}', category='error')
                return redirect(url_for('login'))
        return render_template('login.html', form=form)
    else:
        flash(f"Already logged in as {session['username']}", category='success')
        return redirect(url_for('home'))


@users.route('/<username>', methods=['POST', 'GET'])
def dashboard(username):
    if not session.get('logged_in') or session.get('username') != username:
        return redirect(url_for('login'))
    else:
        quizes = db_query_rows("SELECT * FROM quiz")
        return render_template('user_dashboard.html', quizes=quizes)

@users.route('/listusers', methods=['POST', 'GET'])
def listusers():
    if session.get('is_admin') and session.get('logged_in'):
        with UserRegister() as ur:
            users = ur.get_all_id_username()
        return render_template('admin_dashboard_users.html', users=users)
    elif not session.get('is_admin') and session.get('logged_in'):
        flash('You are not authorized to access this page', category='error')
        return redirect(url_for('/'))
