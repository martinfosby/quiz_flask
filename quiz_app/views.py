from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash

from datetime import datetime
from datetime import timedelta
from . import app


from .forms import *

from .quiz_register import *
from .admin_register import *
from .answer_register import *
from .user_register import *
from .user_has_quiz import *
from .user_has_answer import *
from .mysql_cursor import *
# from .user import User


from .db import *
import werkzeug
import random
# app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(days=7)



# dbconfig = {
#         'host': 'localhost',
#         'user': 'root',
#         'password': 'test',
#         'database': 'quiz_web_app',
#     }




@app.route('/register', methods=["GET", "POST"])
def register() -> 'html':
    form = RegistrationForm()
    if form.validate_on_submit():
        is_admin = form.is_admin.data
        username = form.username.data
        email = form.email.data
        password_hash = werkzeug.generate_password_hash(form.password.data)
        first_name = form.first_name.data
        last_name = form.last_name.data
        db_exec('''INSERT INTO user (is_admin, username, email, password_hash, first_name, last_name) 
        VALUES (%s, %s, %s, %s, %s, %s)''', 
        (is_admin, username, email, password_hash, first_name, last_name))

        # if ar:
        #     flash(f'Successfully created admin {username}', category='success')
        # else:
        #     flash(f'admin already exists {username}', category='failed')
        return redirect(url_for('login'))
        
    return render_template('register.html', form=form)



@app.route('/logout', methods=["GET", "POST"])
def logout() -> 'html':
    if 'username' in session:
        username = session.pop('username')
        admin = session.pop('admin')
        flash(f'logged out as {username} admin {admin}', 'info')
        return redirect(url_for('home'))
    else:
        flash('not logged in', 'info')
        return redirect(url_for('home'))



@app.route('/home')
@app.route("/", methods=('GET', 'POST'))
def home():
    if 'username' in session and 'admin' in session:
        if session['admin'] == False:
            return redirect(url_for('user_dashboard'))
        elif session['admin'] == True:
            return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('login'))
    # return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not 'username' in session:
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            # Check if the user is an admin
            if usertype == 'admin':
                # Redirect to the admin dashboard
                with AdminRegister() as ar:
                    adm = ar.get_admin(username)
                    if adm:
                        session['username'] = username
                        session['admin'] = True
                        session['id'] = adm[0]
                        flash(f'Successfully logged in as admin {username}', category='success')
                        return redirect(url_for('admin_dashboard'))
                    else:
                        flash(f'admin does not exist {username}', category='error')
                        return redirect(url_for('login'))
            else:
                with UserRegister() as ur:
                    usr = ur.get_user(username)
                    if usr:
                        session['username'] = username
                        session['admin'] = False
                        session['id'] = usr[0]
                        flash(f'Successfully logged in as user {username}', category='success')
                        return redirect(url_for('user_dashboard'))
                    else:
                        flash(f'user does not exist {username}', category='error')
                        return redirect(url_for('login'))
        return render_template('login.html', form=form)
    else:
        flash(f"Already logged in as {session['username']}", category='success')
        return redirect(url_for('home'))

@app.route('/quiz/<answer>', methods=['POST', 'GET'])
def process_answer(answer):
    print('hello', answer)
    # if request.method == 'POST' and 'answer' in request.form:
    user_answer = request.form['answer']
        # process the user's answer as needed

    return render_template('admin_dashboard.html', answer=answer, user_answer=user_answer)


@app.route('/admin/dashboard', methods=['POST', 'GET'])
def admin_dashboard():
    with QuizRegister() as qr:
        quizes = qr.get_all_quiz_as_list()
    return render_template('admin_dashboard.html', quizes=quizes)

@app.route('/admin/dashboard/users', methods=['POST', 'GET'])
def admin_dashboard_users():
    with UserRegister() as ur:
        users = ur.get_all_id_username()
    return render_template('admin_dashboard_users.html', users=users)

@app.route('/admin/dashboard/quiz', methods=['GET'])
def admin_dashboard_quiz():
    with MySqlCursor() as mc:
        myselect = mc.execute_select(
            '''
                SELECT username, answer, quiz.id, quiz.title
                FROM user
                INNER JOIN user_has_answer
                ON user.id = user_has_answer.user_id
                INNER JOIN answer
                ON answer.id = user_has_answer.answer_id
                INNER JOIN quiz
                ON answer.quiz_id = quiz.id;
            '''
        )
    # initialize an empty dictionary to store the answers
    quiz_answers = {}

    # loop through the user's answers and group them by quiz name
    for user_answer in myselect:
        username = user_answer[0]
        answer = user_answer[1]
        quiz_id = user_answer[2]
        quiz_name = user_answer[3]
        if quiz_name not in quiz_answers:
            quiz_answers[quiz_name] = {username: [answer]}
        elif username in quiz_answers[quiz_name]:
            quiz_answers[quiz_name][username].append(answer)
        elif username not in quiz_answers[quiz_name]:
            quiz_answers[quiz_name][username] = [answer]


    if request.method == 'GET':
        return render_template('admin_dashboard_quiz.html', quiz_answers=quiz_answers)

@app.route('/admin/dashboard/quiz/edit/<int:id>', methods=['POST', 'GET'])
def admin_dashboard_quiz_edit(id):
    form = QuizForm()
    if form.validate_on_submit():
        # plug inn quez in database
        username = session['username']
        with AdminRegister() as ar:
            admin = ar.get_admin(username)
            with QuizRegister() as qr:
                qr.update_quiz_by_id(
                    id,
                    form.title.data, 
                    form.question.data, 
                    form.active.data, 
                    form.category.data
                )   
            with AnswerRegister() as ans_reg:
                answers = [
                    {'answer': form.answer1.data, 'correct' : form.correct1.data},
                    {'answer': form.answer2.data, 'correct' : form.correct2.data},
                    {'answer': form.answer3.data, 'correct' : form.correct3.data},
                    {'answer': form.answer4.data, 'correct' : form.correct4.data}
                ]
                for i, answer in enumerate(answers):
                    answer_id = ans_reg.get_answer_by_quiz_id(id)
                    ans_reg.update_answer_by_id(answer_id[i][0], answer['answer'], answer['correct'], id)

        flash(f'successfully edited quiz{id}', 'success')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'GET':
        with QuizRegister() as qr:
            quiz = qr.get_quiz_by_id(id)
        with AnswerRegister() as ar:
            answers = ar.get_answer_correct_dict_by_quiz_id(id)
            for answer in answers:
                # convert it so form is correct
                if answer['correct']:
                    answer['correct'] = True
                else:
                    answer['correct'] = False
                answer['csrf_token'] = None
        form.title.data = quiz[1]
        form.question.data = quiz[2]

        form.answer1.data = answers[0]['answer']
        form.correct1.data = answers[0]['correct']
        form.answer2.data = answers[1]['answer']
        form.correct2.data = answers[1]['correct']
        form.answer3.data = answers[2]['answer']
        form.correct3.data = answers[2]['correct']
        form.answer4.data = answers[3]['answer']
        form.correct4.data = answers[3]['correct']

        form.active.data = quiz[3]
        form.category.data = quiz[4]

        return render_template('admin_dashboard_quiz_edit.html', form=form)

@app.route('/admin/dashboard/quiz/delete/<int:quiz_id>', methods=['POST', 'GET'])
def admin_dashboard_quiz_delete(quiz_id):
    # plug inn quez in database
    username = session['username']
    with AdminRegister() as ar:
        admin = ar.get_admin(username)
        if admin:
            # delete in order of foreign keys
            with UserHasQuiz() as uhq:
                uhq_join = uhq.join_user_quiz_with_quiz_id(quiz_id)
                for row in uhq_join:
                    user_id = row[4]
                    uhq.delete_quiz_id(user_id, quiz_id)
            with AnswerRegister() as ar:
                answers_for_quiz_id = ar.get_answer_by_quiz_id(quiz_id)
                with UserHasAnswer() as uha:
                    for ans_row in answers_for_quiz_id:
                        answer_id = ans_row[0]
                        uha_select = uha.get_answer_id(answer_id)
                        for i, row in enumerate(uha_select):
                            user_id = row[0]
                            uha.delete_user_has_answer(user_id, answer_id)
                delete_answer = ar.delete_answer_by_id(quiz_id)
            with QuizRegister() as qr:
                title = qr.get_quiz_title_by_id(quiz_id)
                title = title[0]
                qr.delete_quiz_by_id(quiz_id)

            flash(f'Successfully deleted quiz: {title}', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash(f'this functionality is only available to admins', 'info')
            return redirect(url_for('login'))

    

@app.route('/admin/dashboard/quiz/new', methods=['POST', 'GET'])
def admin_dashboard_quiz_new():
    form = QuizForm()
    if form.validate_on_submit():
        # plug inn quez in database
        username = session['username']
        with AdminRegister() as ar:
            admin = ar.get_admin(username)
            with QuizRegister() as qr:
                qr.create_quiz(
                    title=form.title.data, 
                    question=form.question.data, 
                    active=form.active.data, 
                    category=form.category.data,
                    admin_id=admin[0]
                    )
                quiz = qr.get_all_quiz()
                quiz_id = quiz[-1][0] # get last quiz
            with AnswerRegister() as ans_reg:
                answers = [
                    {'answer': form.answer1.data, 'correct' : form.correct1.data},
                    {'answer': form.answer2.data, 'correct' : form.correct2.data},
                    {'answer': form.answer3.data, 'correct' : form.correct3.data},
                    {'answer': form.answer4.data, 'correct' : form.correct4.data}
                ]
                for answer in answers:
                    ans_reg.create_answer_for_quiz(answer['answer'], answer['correct'], quiz_id)

        flash('successfully created quiz', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_dashboard_quiz_new.html', form=form)


@app.route('/user/dashboard')
def user_dashboard():
    # return render_template('user_dashboard.html')
    return redirect(url_for('user_dashboard_quiz_view'))

@app.route('/user/dashboard/quiz/<int:quiz_id>', methods=['POST', 'GET'])
@app.route('/user/dashboard/quiz', methods=['POST', 'GET'])
def user_dashboard_quiz_view(quiz_id = 1):
    with QuizRegister() as qr:
        quiz = qr.get_quiz_by_id(quiz_id)
        length_quizes = qr.get_length_all_quizes()[0] # used later

    with AnswerRegister() as ar:
        quiz_id = quiz[0]
        answers = ar.get_answer_dict_by_quiz_id(quiz_id)
        random.shuffle(answers)
        quiz = list(quiz)
        quiz.append(answers)

    if request.method == 'GET':
        form = SelectForm()
        # reset form.answer.choices
        if form.answer.choices:
            form.answer.choices = []

        for answer in quiz[6]:
            form.answer.choices.append((answer['correct'], answer['answer'], answer['id']))

        return render_template('user_dashboard_quiz_view.html', quiz=quiz , form=form, length_quizes=length_quizes)

    if request.method == 'POST':

        submit = request.form['submit']

        if not session.get('quiz_answers'):
            session['quiz_answers'] = []
        session_answer = session['quiz_answers']

        if request.form.get('answer'):
            form_answer, form_label, form_answer_id, form_quiz_title = eval(request.form['answer'])
            # session[f'quiz-{quiz_id}-answers'] = (form_answer, form_label, form_answer_id, form_quiz_title)
            session_answer.append((form_answer, form_label, form_answer_id, form_quiz_title))
            session['quiz_answers'] = session_answer
        else:
            session_answer.append((None, None, None, None))
            session['quiz_answers'] = session_answer


        if submit == 'prev':
            return redirect(url_for('user_dashboard_quiz_view', quiz_id=quiz_id-1))
        elif submit == 'next':
            return redirect(url_for('user_dashboard_quiz_view', quiz_id=quiz_id+1))
        elif submit == 'send in':
            user_id = session['id']
            with UserHasAnswer() as uha:
                for answer in session['quiz_answers']:
                    answer_id = answer[2]
                    inserted = uha.insert_into(user_id, answer_id)
            
            del session['quiz_answers']
            flash(f'You have sent in all your answers', category='success')
            return redirect(url_for('user_dashboard'))
        elif submit == 'exit':
            del session['quiz_answers']
            flash(f'You have exited no answer have been submited', category='danger')
            return redirect(url_for('user_dashboard'))




@app.route('/user/dashboard/quizes', methods=['POST', 'GET'])
def user_dashboard_quiz():
    with QuizRegister() as qr:
        quizes = qr.get_all_quiz_as_list()

    for quiz in quizes:
        with AnswerRegister() as ar:
            quiz_id = quiz[0]
            answers = ar.get_answer_dict_by_quiz_id(quiz_id)
            random.shuffle(answers)
            quiz.append(answers)


    if request.method == 'GET':
        form_list = []
        for i in range(len(quizes)):
            form = RadioForm()
            for answer in quizes[i][6]:
                form.answer.choices.append((answer['correct'], answer['answer'], answer['id']))
            # form.answers.choices = quizes[i][6]
            form.answer.id += ('-' + str(i))

            form_list.append(form)
        return render_template('user_dashboard_quiz.html', quizes=quizes, form_list=form_list)

    if request.method == 'POST':
        form_answer, form_label, form_answer_id, form_quiz_title = eval(request.form['answer'])
        user_id = session['id']
        with UserHasAnswer() as uq:
            if not uq.insert_into(user_id, form_answer_id):
                flash(f'you already have enter that answer for quiz: {form_quiz_title}', category='info')
            else:
                flash('Answer submited', category='info')
        if form_answer:
            flash(f'You have entered the right answer: {form_label} for quiz: {form_quiz_title}', category='success')
        else:
            flash(f'You have entered the wrong answer: {form_label} for quiz: {form_quiz_title}', category='danger')
        return redirect(url_for('user_dashboard'))


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")