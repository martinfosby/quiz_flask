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
import uuid

# @users.route('/', methods=['POST', 'GET'])
# def home():
#     if session.get('id'):
#         user = get_user_by_id(session.get('id'))
#         if 
#         return render_template('home.html')
#     else:
#         return redirect(url_for('users.login_user_type'))


@users.route('/register', methods=["GET", "POST"])
def register():
    check_logged_in()
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password_hash = werkzeug.security.generate_password_hash(form.password.data)
        first_name = form.first_name.data
        last_name = form.last_name.data
        is_admin = form.is_admin.data
        db_exec('''INSERT INTO user (username, email, password_hash, first_name, last_name, is_admin) 
        VALUES (%s, %s, %s, %s, %s, %s)''', 
        (username, email, password_hash, first_name, last_name, is_admin))
        flash(f'Successfully created admin {username}', category='success')
        return redirect(url_for('home'))
        
    return render_template('users/register.html', form=form)



@users.route('/logout', methods=["GET", "POST"])
def logout():
    if session.get('logged_in'):
        usr = db_query_single("SELECT * FROM administrator WHERE id=%s", [session['id']])
        session.clear() # clear the rest
        if usr.is_admin:
            flash(f'logged out as admin {usr.username}', 'info')
        else:
            flash(f'logged out as user', 'info')
        return redirect(url_for('home'))
    else:
        flash('not logged in', 'info')
        return redirect(url_for('users.login'))


# @users.route('/login/user/type', methods=['GET', 'POST'])
# def login_user_type():
#     user_type_form = UserTypeForm()
#     if user_type_form.validate_on_submit():
#         if user_type_form.usertype.data == 'admin':
#             return redirect(url_for('users.login'))

#     else:
#         return render_template('user_type.html', user_type_form=user_type_form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get('id'):
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = db_query_single("SELECT * FROM user WHERE username=%s", [username])
            if user:
                if werkzeug.security.check_password_hash(user.get('password_hash'), password):
                    session['id'] = user.get('id')
                    flash(f'Successfully logged in as admin {username}', category='success')
                    return redirect(url_for('home'))
                else:
                    flash('Incorrect password', category='error')
                    return redirect(url_for('users.login'))
            else:
                flash(f'user does not exist {username}', category='error')
                return redirect(url_for('users.login'))
        return render_template('users/login.html', form=form)
    else:
        flash(f"Already logged in", category='success')
        return redirect(url_for('home'))


@users.route('/list', methods=['POST', 'GET'])
def list():
    if session.get('logged_in'):
        users = db_query_rows("SELECT * FROM user")
        return render_template('admin_dashboard_users.html', users=users)
    else:
        flash('You are not authorized to access this page', category='error')
        return redirect(url_for('/'))

@users.route('/create', methods=['POST', 'GET'])
def create():
    user = db_query_single("SELECT * FROM user WHERE id=%s", [session.get('id')])
    if user.get('is_admin'):
        form = QuizForm()
        if form.validate_on_submit():
            title = form.title.data
            active = form.active.data
            comment = form.comment.data
            conn = db_get_connection()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO quiz (title, active, comment) VALUES (%s, %s, %s);''', [title, active, comment])
            quiz_id = cursor.lastrowid
            conn.commit();cursor.close();conn.close()
            flash(f'successfully created quiz {title}', 'success')
            return redirect(url_for('questions.create_question', quiz_id=quiz_id))
        return render_template('quizes/create.html', form=form)
    else:
        flash('you are not an admin', 'danger')
        return redirect(url_for('home'))

@users.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    if check_admin():
        form = QuizForm()
        if form.validate_on_submit():
            title = form.title.data
            active = form.active.data
            comment = form.comment.data
            db_exec('''UPDATE quiz SET title=%s, active=%s, comment=%s WHERE id=%s''', [title, active, comment, id])
            flash(f'successfully edited quiz{title}', 'success')
            return redirect(url_for('home'))
        
        if request.method == 'GET':
            quiz = db_query_single("SELECT * FROM quiz WHERE id=%s", [id])
            form.title.data = quiz['title']
            form.active.data = quiz['active']
            form.comment.data = quiz['comment']

            return render_template('quizes/update.html', form=form)

@users.route('/read/<int:id>', methods=['POST', 'GET'])
def read(id):
    if request.method == 'GET':
        user = db_query_single("SELECT * FROM user WHERE id=%s", [id])
        user_answers = db_query_rows("SELECT * FROM user_has_answer WHERE id=%s", [id])
        return render_template('users/read.html')


@users.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    # delete on cascade
    user = db_query_single("SELECT * FROM user WHERE id=%s", [session.get('id')])
    if user.get('is_admin'):
        db_exec('''DELETE FROM user WHERE id=%s''', [id])
        flash(f'Successfully deleted user: {id}', 'success')
        return redirect(url_for('home'))
    else:
        flash(f'this functionality is only available to admins', 'info')
        return redirect(url_for('home'))
