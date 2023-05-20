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
from ..db import db_query_rows

import random

quizes = Blueprint('quizes', __name__, url_prefix='/quizes')

@quizes.route('/quiz', methods=['GET'])
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

@quizes.route('/edit/<int:id>', methods=['POST', 'GET'])
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

@quizes.route('/delete/<int:quiz_id>', methods=['POST', 'GET'])
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

    

@quizes.route('/new', methods=['POST', 'GET'])
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




@quizes.route('/listquizes', methods=['POST', 'GET'])
def listquizes():
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