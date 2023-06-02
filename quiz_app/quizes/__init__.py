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


@quizes.route('/index')
@quizes.route('/home')
@quizes.route('/')
def home():
    user = db_query_single("SELECT * FROM user WHERE id=%s", [session.get('id')])
    quizes = db_query_rows("SELECT * FROM quiz")

    current_user_has_quiz = db_query_rows("SELECT * FROM user_has_quiz INNER JOIN user ON user_id=user.id WHERE user_id=%s", [session.get('id')])
    current_user_quizes = {}
    if current_user_has_quiz:
        for list in current_user_has_quiz:
            current_user_quizes[list['quiz_id']] = db_query_single("SELECT * FROM user_has_quiz INNER JOIN user ON user_id=user.id WHERE quiz_id=%s", [list['quiz_id']])

    if user.get('is_admin'):
        user_has_quiz = db_query_rows("SELECT * FROM user_has_quiz INNER JOIN user ON user_id=user.id")
        users_quizes = {}
        for list in user_has_quiz:
            users_quizes[list['quiz_id']] = db_query_rows("SELECT * FROM user_has_quiz INNER JOIN user ON user_id=user.id WHERE quiz_id=%s", [list['quiz_id']])

        return render_template('quizes/home.html', quizes=quizes, users_quizes=users_quizes, current_user_quizes=current_user_quizes)
    else:
        return render_template('quizes/home.html', quizes=quizes, current_user_quizes=current_user_quizes)


@quizes.route('/user/answers', methods=['GET'])
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
@admin_required
def create_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        title = form.title.data
        active = form.active.data
        quiz_id = db_exec('''INSERT INTO quiz (title, active) VALUES (%s, %s);''', [title, active])
        flash(f'successfully created quiz {title}', 'success')
        return redirect(url_for('questions.create_question', quiz_id=quiz_id))
    return render_template('quizes/create.html', form=form)

@quizes.route('/update/<int:id>', methods=['POST', 'GET'])
def update_quiz(id):
    form = QuizForm()
    if form.validate_on_submit():
        if request.form.get('submit') == 'Update':
            title = form.title.data
            active = form.active.data
            comment = form.comment.data
            db_exec('''UPDATE quiz SET title=%s, active=%s, comment=%s WHERE id=%s''', [title, active, comment, id])
            flash(f'successfully updated quiz {title}', 'success')
        elif request.form.get('submit') == 'Cancel':
            flash(f'successfully cancelled', 'success')
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        quiz = db_query_single("SELECT * FROM quiz WHERE id=%s", [id])
        form.title.data = quiz['title']
        form.active.data = quiz['active']
        form.comment.data = quiz['comment']

        return render_template('quizes/update.html', form=form)

@quizes.route('/<user_id>/quiz/<int:quiz_id>/approve/<int:approved>', methods=['POST', 'GET'])
@admin_required
def approve(user_id, approved, quiz_id):
    form = TextAreaForm()
    if form.validate_on_submit():
        comment = form.text.data
        db_exec('''UPDATE user_has_quiz SET approved=%s, comment=%s WHERE user_id=%s AND quiz_id=%s''', [approved, comment, user_id, quiz_id])
        flash(f'Successfully approved quiz {quiz_id}', category='success')
        return redirect(url_for('quizes.home'))
    return render_template('quizes/approve.html', form=form)

@quizes.route('/review/<int:id>', methods=['POST', 'GET'])
def review(id):
    quiz = db_query_single("SELECT * FROM quiz WHERE id=%s", [id])
    questions = db_query_rows('''SELECT * FROM question WHERE id IN (SELECT DISTINCT(answer_question_id) FROM user_has_answer WHERE answer_question_quiz_id=%s);''', [id])
    user_has_question = db_query_rows('''SELECT * FROM user_has_question WHERE question_quiz_id=%s;''', [id])
    # user_ids = [user['user_id'] for user in user_has_question]

    users_answers = {}
    for question in questions:
        users_answers[question['id']] = db_query_rows('''
        SELECT user_id, answer_id, answer_question_id as question_id, answer_question_quiz_id as quiz_id, essay, username, answer.answer, question.title, question.content, question.answer_type, question.category
        FROM user_has_answer 
        INNER JOIN user ON user_id=user.id 
        INNER JOIN answer ON answer_id=answer.id
        INNER JOIN question ON question_id=question.id
        WHERE answer_question_id=%s;''', [question['id']])
    
    return render_template('quizes/review.html', users_answers=users_answers, quiz=quiz)

@quizes.route('/read/<int:id>', methods=['POST', 'GET'])
def read_quiz(id):
    user_id=session.get('id')
    if request.method == 'POST':
        if request.form.get('type') != 'essay':
            answer_ids = request.form.getlist('answer')
            for answer_id in answer_ids:
                answer_id = int(answer_id)
                answer = db_query_single("SELECT * FROM answer WHERE id=%s", [answer_id])
                question_id = answer['question_id']
                db_exec('''INSERT INTO user_has_answer (user_id, answer_id, answer_question_id, answer_question_quiz_id) VALUES (%s, %s, %s, %s)''', [session.get('id'), answer_id, question_id, id])
                db_exec('''INSERT INTO user_has_question (user_id, question_id, question_quiz_id, is_answered) VALUES (%s, %s, %s, %s)''', [session.get('id'), question_id, id, 1])
                flash(f'succesfully inserted answer {answer_id} for question {question_id} for quiz {id}', 'success')
            if not answer_ids:
                flash('you must select at least one answer', 'danger')
        else:
            keys_values_ending_with_text = [value for key, value in request.form.items() if key.endswith('text')]
            keys_values_ending_with_id = [value for key, value in request.form.items() if key.endswith('id')]

            zipped_pairs = zip(keys_values_ending_with_id, keys_values_ending_with_text)

            for key, value in zipped_pairs:
                answer_id = key
                question_id = db_query_single("SELECT question_id FROM answer WHERE id=%s", [answer_id])['question_id']
                essay = value
                db_exec('''INSERT INTO user_has_answer (user_id, answer_id, answer_question_id, answer_question_quiz_id, essay) VALUES (%s, %s, %s, %s, %s)''', [session.get('id'), answer_id, question_id, id, essay])
                db_exec('''INSERT INTO user_has_question (user_id, question_id, question_quiz_id, is_answered) VALUES (%s, %s, %s, %s)''', [session.get('id'), question_id, id, 1])
                flash(f'succesfully inserted answer {answer_id} for question {question_id} for quiz {id}', 'success')

        return redirect(url_for('quizes.read_quiz', id=id))

    if request.method == 'GET':
        quiz = db_query_single("SELECT * FROM quiz WHERE id=%s", [id])
        quiz_completed = db_query_single("SELECT * FROM user_has_quiz WHERE user_id=%s AND quiz_id=%s", [session.get('id'), id])
        if quiz_completed:
            if quiz_completed.get( 'is_completed' ):
                flash(f'you have completed all questions from {quiz.get("title")}', 'success')
                return redirect(url_for('quizes.home'))
        questions = db_query_rows("SELECT * FROM question WHERE quiz_id=%s", [id])
        # questions_not_answered = db_query_rows("SELECT question.*, user_id, is_answered FROM `question` LEFT JOIN user_has_question as uhq ON id=uhq.question_id WHERE uhq.is_answered IS NULL AND quiz_id = %s", [id])
        # if not questions_not_answered:
        #     db_exec('''INSERT INTO user_has_quiz (user_id, quiz_id, is_completed) VALUES (%s, %s, %s)''', [session.get('id'), id, 1])
        #     flash('you have completed all questions', 'success')
        #     return redirect(url_for('quizes.home'))
        # if id not in [q['id'] for q in questions_not_answered]:
        #     return redirect(url_for('questions.read_question', id=questions_not_answered[0]['id'], quiz_id=id))
        # answers = db_query_rows("SELECT * FROM answer WHERE question_quiz_id=%s", [id])
        answers = {}
        forms = {}
        is_answered = {}
        for question in questions:
            is_answered[question['id']] = db_query_single("SELECT is_answered FROM user_has_question WHERE user_id=%s AND question_id=%s AND question_quiz_id=%s", [session.get('id'), question['id'], id])
            answers[question['id']] = db_query_rows("SELECT * FROM answer WHERE question_id=%s AND question_quiz_id=%s ORDER BY RAND()", [question['id'], id])
            if answers[question['id']]:
                if question['answer_type'] == 'single':
                    form = RadioForm()
                    for answer in answers[question['id']]:
                        form.answer.choices.append((answer['id'], answer['answer']))
                elif question['answer_type'] == 'multiple':
                    form = CheckBoxForm()
                    for answer in answers[question['id']]:
                        form.answer.choices.append((answer['id'], answer['answer']))
                elif question['answer_type'] == 'essay':
                    form = MultipleTextAreaForm()
                    for answer in answers[question['id']]:
                        form.answer.append_entry()
                        form.answer.entries[-1].form.text.data = answer['answer']
                        form.answer.entries[-1].form.id.data = str(answer['id'])

                forms[question['id']] = form
        return render_template('quizes/read.html', quiz=quiz, questions=questions, answers=answers, forms=forms, is_answered=is_answered)


@quizes.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_quiz(id):
    # delete on cascade
    user = get_user()
    if user.get('is_admin'):
        if request.method == 'POST':
            if request.form.get('submit') == 'delete':
                db_exec('''DELETE FROM quiz WHERE id=%s''', [id])
                flash(f'Successfully deleted quiz: {id}', 'success')
            elif request.form.get('submit') == 'cancel':
                flash(f'Successfully cancelled: {id}', 'success')
            return redirect(url_for('home'))
        elif request.method == 'GET':
            return render_template('quizes/delete.html', id=id)
    else:
        flash(f'this functionality is only available to admins', 'info')
        return redirect(url_for('home'))

    




# @quizes.route('/<int:quiz_id>', methods=['POST', 'GET'])
# @quizes.route('/quiz', methods=['POST', 'GET'])
# def quiz_view(quiz_id = 1):
#     with QuizRegister() as qr:
#         quiz = qr.get_quiz_by_id(quiz_id)
#         length_quizes = qr.get_length_all_quizes()[0] # used later

#     with AnswerRegister() as ar:
#         quiz_id = quiz[0]
#         answers = ar.get_answer_dict_by_quiz_id(quiz_id)
#         random.shuffle(answers)
#         quiz = list(quiz)
#         quiz.append(answers)

#     if request.method == 'GET':
#         form = SelectForm()
#         # reset form.answer.choices
#         if form.answer.choices:
#             form.answer.choices = []

#         for answer in quiz[6]:
#             form.answer.choices.append((answer['correct'], answer['answer'], answer['id']))

#         return render_template('user_dashboard_quiz_view.html', quiz=quiz , form=form, length_quizes=length_quizes)

#     if request.method == 'POST':

#         submit = request.form['submit']

#         if not session.get('quiz_answers'):
#             session['quiz_answers'] = []
#         session_answer = session['quiz_answers']

#         if request.form.get('answer'):
#             form_answer, form_label, form_answer_id, form_quiz_title = eval(request.form['answer'])
#             # session[f'quiz-{quiz_id}-answers'] = (form_answer, form_label, form_answer_id, form_quiz_title)
#             session_answer.append((form_answer, form_label, form_answer_id, form_quiz_title))
#             session['quiz_answers'] = session_answer
#         else:
#             session_answer.append((None, None, None, None))
#             session['quiz_answers'] = session_answer


#         if submit == 'prev':
#             return redirect(url_for('user_dashboard_quiz_view', quiz_id=quiz_id-1))
#         elif submit == 'next':
#             return redirect(url_for('user_dashboard_quiz_view', quiz_id=quiz_id+1))
#         elif submit == 'send in':
#             user_id = session['id']
#             with UserHasAnswer() as uha:
#                 for answer in session['quiz_answers']:
#                     answer_id = answer[2]
#                     inserted = uha.insert_into(user_id, answer_id)
            
#             del session['quiz_answers']
#             flash(f'You have sent in all your answers', category='success')
#             return redirect(url_for('user_dashboard'))
#         elif submit == 'exit':
#             del session['quiz_answers']
#             flash(f'You have exited no answer have been submited', category='danger')
#             return redirect(url_for('user_dashboard'))




# @quizes.route('/list', methods=['POST', 'GET'])
# def list():
#     quizes = db_query_rows("SELECT * FROM quiz")

#     for quiz in quizes:
#         quiz_id = quiz[0]
#         questions = db_query_rows("SELECT * FROM question WHERE quiz_id=%s", [quiz_id])
#         answers = db_query_rows("SELECT * FROM answer WHERE question_quiz_id=%s ORDER BY RAND()", [quiz_id])


#     if request.method == 'GET':
#         form_list = []
#         for i in range(len(quizes)):
#             form = RadioForm()
#             for answer in quizes[i][6]:
#                 form.answer.choices.append((answer['correct'], answer['answer'], answer['id']))
#             # form.answers.choices = quizes[i][6]
#             form.answer.id += ('-' + str(i))

#             form_list.append(form)
#         return render_template('user_dashboard_quiz.html', quizes=quizes, form_list=form_list)

#     if request.method == 'POST':
#         form_answer, form_label, form_answer_id, form_quiz_title = eval(request.form['answer'])
#         user_id = session['id']
#         with UserHasAnswer() as uq:
#             if not uq.insert_into(user_id, form_answer_id):
#                 flash(f'you already have enter that answer for quiz: {form_quiz_title}', category='info')
#             else:
#                 flash('Answer submited', category='info')
#         if form_answer:
#             flash(f'You have entered the right answer: {form_label} for quiz: {form_quiz_title}', category='success')
#         else:
#             flash(f'You have entered the wrong answer: {form_label} for quiz: {form_quiz_title}', category='danger')
#         return redirect(url_for('user_dashboard'))