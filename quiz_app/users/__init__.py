from flask import Blueprint, session, render_template, redirect, url_for, request, flash, g

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

import werkzeug


# @users.after_request
# def after_request(response):
#     # Modify the response based on the data in g
#     user = g.user
#     response.headers['X-User'] = user

@users.route('/', methods=['POST', 'GET'])
@admin_required
def home():
    users = db_query_rows("SELECT * FROM user")
    return render_template('users/home.html', users=users)


@users.route('/profile')
@login_required
def profile():
    # Access the user from the g object
    user = g.user

    # If the user is not stored in g, retrieve the user based on the session
    if not user:
        user_id = session.get('id')
        if user_id:
            user = get_user_by_id(user_id)
            g.user = user

    if user:
        return f"Welcome, {user['username']}!"
    else:
        return 'Unauthorized'



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
@login_required
def logout():
    user = get_user()
    session.clear() # clear the rest
    if user.get('is_admin'):
        flash(f'logged out as admin {user.get("username")}', 'info')
    elif user.get('is_regular'):
        flash(f'logged out as user', 'info')
    elif user.get('is_anonymous'):
        flash(f'logged out as guest', 'info')
    return redirect(url_for('home'))


@users.route('/login/user/type', methods=['GET', 'POST'])
def login_user_type():
    form = UserTypeForm()
    if form.validate_on_submit():
        if form.usertype.data == 'admin':
            return redirect(url_for('users.login'))
        elif form.usertype.data == 'user':
            return redirect(url_for('users.login'))
        elif form.usertype.data == 'guest':
            session['id'] = db_exec('''INSERT INTO user (is_anonymous, is_regular, is_admin) VALUES (%s, %s, %s)''', (1,0,0))
            return redirect(url_for('home'))
        else:
            flash(f'Invalid user type { form.usertype.data}', category='error')
            return redirect(url_for('users.login_user_type'))
    else:
        return render_template('user_type.html', form=form)


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
                    if user.get('is_admin'):
                        flash(f'Successfully logged in as admin {username}', category='success')
                    else:
                        flash(f'Successfully logged in as user {username}', category='success')
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



@users.route('/create', methods=['POST', 'GET'])
@admin_required
def create():
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

@users.route('/update/<int:id>', methods=['POST', 'GET'])
@admin_required
def update(id):
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
@admin_required
def delete(id):
    # delete on cascade
    user = db_query_single("SELECT * FROM user WHERE id=%s", [session.get('id')])
    db_exec('''DELETE FROM user WHERE id=%s''', [id])
    flash(f'Successfully deleted user: {id}', 'success')
    return redirect(url_for('home'))
