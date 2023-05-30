from flask import Flask, render_template, request, session, redirect, url_for, flash, Blueprint

from ..forms import QuestionForm

from ..db import *
from ..utils import *


questions = Blueprint('questions', __name__, url_prefix='/questions')


@questions.route('/create/<int:quiz_id>', methods=['POST', 'GET'])
def create_question(quiz_id):
    form = QuestionForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        answer_type = form.answer_type.data
        category = form.category.data
        question_id = db_exec('''INSERT INTO question (quiz_id, title, content, answer_type, category) 
        VALUES (%s, %s, %s, %s, %s)''', 
        (quiz_id, title, content, answer_type, category))
        flash(f'Successfully created question {title} for quiz {quiz_id}', category='success')
        if answer_type != 'essay':
            return redirect(url_for('answers.create_answer', quiz_id=quiz_id, question_id=question_id))
        else: 
            return redirect(url_for('quizes.read_quiz', id=quiz_id))
    return render_template('questions/create.html', form=form, quiz_id=quiz_id)

@questions.route('/read/<int:quiz_id>', methods=['GET'])
def read_questions_from_quiz(id, quiz_id):
    questions = db_query_rows("SELECT * FROM question WHERE quiz_id=%s", [quiz_id])
    return render_template('questions/read.html', questions=questions)

@questions.route('/read/<int:id>', methods=['GET'])
def read_question(id):
    question = db_query_single("SELECT * FROM question WHERE id=%s", [id])
    return render_template('questions/read.html', question=question)


@questions.route('/update/<int:id>', methods=['POST', 'GET'])
def update_question(id):
    question = db_query_single("SELECT * FROM question WHERE id=%s", [id])
    form = QuestionForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        answer_type = form.answer_type.data
        category = form.category.data
        db_exec('''UPDATE question SET title=%s, content=%s, answer_type=%s, category=%s WHERE id=%s''', 
        (title, content, answer_type, category, id))
        flash(f'Successfully updated question {title}', category='success')
        return redirect(url_for('questions.read_question', id=id))
    
    form.title.data = question['title']
    form.content.data = question['content']
    form.answer_type.data = question['answer_type']
    form.category.data = question['category']
    
    return render_template('questions/update.html', question=question)


@questions.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_question(id):
    user = get_user()
    if user.get('is_admin'):
        if request.method == 'POST':
            if request.form.get('submit') == 'delete':
                db_exec('''DELETE FROM question WHERE id=%s''', [id])
                flash(f'Successfully deleted question: {id}', 'success')
                return redirect(url_for('home'))
            elif request.form.get('submit') == 'cancel':
                flash(f'Successfully cancelled: {id}', 'success')
                return redirect(url_for('home'))
        elif request.method == 'GET':
            return render_template('questions/delete.html', id=id)
    else:
        flash(f'this functionality is only available to admins', 'info')
        return redirect(url_for('home'))

