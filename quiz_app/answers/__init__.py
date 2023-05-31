from flask import Flask, render_template, request, session, redirect, url_for, flash, Blueprint

from ..forms import AnswerForm

from ..db import *
from ..utils import *


answers = Blueprint('answers', __name__, url_prefix='/answers')

@answers.route('/create/<int:quiz_id>/<int:question_id>', methods=['POST', 'GET'])
def create_answer(quiz_id, question_id):
    form = AnswerForm()
    if form.validate_on_submit():
        answer = form.answer.data
        comment = form.comment.data
        correct = form.correct.data
        answer_id = db_exec('''INSERT INTO answer (question_id, question_quiz_id, answer, comment, correct) 
        VALUES (%s, %s, %s, %s, %s)''', 
        (question_id, quiz_id, answer, comment, correct))
        flash(f'Successfully created answer {answer} for question {question_id} for quiz {quiz_id}', category='success')
        return redirect(url_for('answers.create_answer', quiz_id=quiz_id, question_id=question_id))
    return render_template('answers/create.html', form=form, quiz_id=quiz_id, question_id=question_id)

@answers.route('/read/<int:quiz_id>/<int:question_id>', methods=['GET'])
def read_answers_from_question(quiz_id, question_id):
    answers = db_query_rows("SELECT * FROM answer WHERE quiz_id=%s AND question_id=%s", [quiz_id, question_id])
    return render_template('answers/read.html', answers=answers)

@answers.route('/read/<int:id>', methods=['GET'])
def read_answer(id):
    answer = db_query_single("SELECT * FROM answer WHERE id=%s", [id])
    return render_template('answers/read.html', answer=answer)


@answers.route('/update/<int:id>', methods=['POST', 'GET'])
def update_answer(id):
    question = db_query_single("SELECT * FROM question WHERE id=%s", [id])
    form = AnswerForm()
    if form.validate_on_submit():
        answer = form.answer.data
        comment = form.comment.data
        correct = form.correct.data
        db_exec('''UPDATE answer SET answer=%s, comment=%s, correct=%s WHERE id=%s''', 
        (answer, comment, correct, id))
        flash(f'Successfully updated answer {answer}', category='success')
        return redirect(url_for('answers.read_answer', id=id))
    
    form.title.data = question['title']
    form.content.data = question['content']
    form.answer_type.data = question['answer_type']
    form.category.data = question['category']
    
    return render_template('questions/update.html', question=question)


@answers.route('/delete/<int:id>', methods=['GET'])
def delete_answer(id):
    user = get_user()
    if user.get('is_admin'):
        if request.method == 'POST':
            db_exec('''DELETE FROM answer WHERE id=%s''', [id])
            flash(f'Successfully deleted answer: {id}', 'success')
            return redirect(url_for('home'))
        elif request.method == 'GET':
            return render_template('answers/delete.html', id=id)
    else:
        flash(f'this functionality is only available to admins', 'info')
        return redirect(url_for('home'))

