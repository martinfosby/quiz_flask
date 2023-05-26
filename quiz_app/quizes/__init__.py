from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from quiz_app.mysql_cursor import MySqlCursor
from quiz_app.forms import *

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

quizes = Blueprint('quizes', __name__, url_prefix='/quizes')

@quizes.route('/quiz', methods=['GET'])
def quiz():
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

@quizes.route('/create', methods=['POST', 'GET'])
def create_quiz():
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

@quizes.route('/update/<int:id>', methods=['POST', 'GET'])
def update_quiz(id):
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

@quizes.route('/read/<int:id>', methods=['POST', 'GET'])
def read_quiz(id):
    if request.method == 'GET':
        quiz = db_query_single("SELECT * FROM quiz WHERE id=%s", [id])
        questions = db_query_rows("SELECT * FROM question WHERE quiz_id=%s", [id])
        answers_for_quiz = db_query_rows("SELECT * FROM answer WHERE quiz_id=%s", [id])
        return render_template('quizes/read.html', quiz=quiz, questions=questions)


@quizes.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_quiz(id):
    # delete on cascade
    user = db_query_single("SELECT * FROM user WHERE id=%s", [session.get('id')])
    if user.get('is_admin'):
        db_exec('''DELETE FROM quiz WHERE id=%s''', [id])
        flash(f'Successfully deleted quiz: {id}', 'success')
        return redirect(url_for('home'))
    else:
        flash(f'this functionality is only available to admins', 'info')
        return redirect(url_for('home'))

    




@quizes.route('/<int:quiz_id>', methods=['POST', 'GET'])
@quizes.route('/quiz', methods=['POST', 'GET'])
def quiz_view(quiz_id = 1):
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




@quizes.route('/list', methods=['POST', 'GET'])
def list():
    quizes = db_query_rows("SELECT * FROM quiz")

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