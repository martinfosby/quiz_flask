from flask import render_template, request, session, redirect, url_for, flash, Blueprint

from ..forms import *

from ..db import *
from ..utils import *


questions = Blueprint('questions', __name__, url_prefix='/questions')

    


@questions.get('/')
@admin_required
def home():
    questions = db_query_rows("SELECT * FROM question")
    return render_template('questions/home.html', questions=questions)

@questions.route('/create/<int:quiz_id>', methods=['POST', 'GET'])
@admin_required
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
        return redirect(url_for('answers.create_answer', quiz_id=quiz_id, question_id=question_id))
    return render_template('questions/create.html', form=form, quiz_id=quiz_id)

@questions.route('/read/<int:id>', methods=['GET', 'POST'])
def read_question(id):
    if request.args.get('quiz_id'):
        quiz_id = request.args.get('quiz_id')
    else:
        quiz_id = db_query_single('''SELECT quiz_id FROM question WHERE id=%s''', [id])['quiz_id']

    if request.method == 'POST':
        if request.form.get('type') != 'essay':
            answer_ids = request.form.getlist('answer')
            for answer_id in answer_ids:
                answer_id = int(answer_id)
                answer = db_query_single("SELECT * FROM answer WHERE id=%s", [answer_id])
                question_id = answer['question_id']
                db_exec('''INSERT INTO user_has_answer (user_id, answer_id, answer_question_id, answer_question_quiz_id) VALUES (%s, %s, %s, %s)''', [session.get('id'), answer_id, question_id, quiz_id])
                db_exec('''INSERT INTO user_has_question (user_id, question_id, question_quiz_id, is_answered) VALUES (%s, %s, %s, %s)''', [session.get('id'), question_id, quiz_id, 1])
                flash(f'succesfully inserted answer {answer_id} for question {question_id} for quiz {id}', 'success')
            if not answer_ids:
                flash('you must select at least one answer', 'danger')
        else:
            keys_values_ending_with_text = [value for key, value in request.form.items() if key.endswith('text')]
            keys_values_ending_with_id = [value for key, value in request.form.items() if key.endswith('id')]

            zipped_pairs = zip(keys_values_ending_with_id, keys_values_ending_with_text)

            for key, value in zipped_pairs:
                answer_id = key
                essay = value
                db_exec('''INSERT INTO user_has_answer (user_id, answer_id, answer_question_id, answer_question_quiz_id, essay) VALUES (%s, %s, %s, %s, %s)''', [session.get('id'), answer_id, id, quiz_id, essay])
                db_exec('''INSERT INTO user_has_question (user_id, question_id, question_quiz_id, is_answered) VALUES (%s, %s, %s, %s)''', [session.get('id'), id, quiz_id, 1])
                flash(f'succesfully inserted answer {answer_id} for question {id} for quiz {id}', 'success')

        return redirect(url_for('questions.read_question', id=id, quiz_id=quiz_id))

    elif request.method == 'GET':
        question = db_query_single("SELECT * FROM question WHERE id=%s", [id])

        questions_not_answered = db_query_rows("SELECT question.*, user_id, is_answered FROM `question` LEFT JOIN user_has_question as uhq ON id=uhq.question_id WHERE uhq.is_answered IS NULL AND quiz_id = %s", [quiz_id])
        if not questions_not_answered:
            db_exec('''INSERT INTO user_has_quiz (user_id, quiz_id, is_completed) VALUES (%s)''', [quiz_id, 1])
            return redirect(url_for('quizes.home'))
        if id not in [q['id'] for q in questions_not_answered]:
            return redirect(url_for('questions.read_question', id=questions_not_answered[0]['id'], quiz_id=quiz_id))
        answers = db_query_rows("SELECT * FROM answer WHERE question_id=%s ORDER BY RAND()", [id])

        if answers:
            if question['answer_type'] == 'single':
                form = RadioForm()
                for answer in answers:
                    form.answer.choices.append((answer['id'], answer['answer']))
            elif question['answer_type'] == 'multiple':
                form = CheckBoxForm()
                for answer in answers:
                    form.answer.choices.append((answer['id'], answer['answer']))
            elif question['answer_type'] == 'essay':
                form = MultipleTextAreaForm()
                for answer in answers:
                    form.answer.append_entry()
                    form.answer.entries[-1].form.text.data = answer['answer']
                    form.answer.entries[-1].form.id.data = str(answer['id'])
            else:
                abort(404)

    return render_template('questions/read.html', question=question, answers=answers, form=form)


@questions.route('/update/<int:id>', methods=['POST', 'GET'])
@admin_required
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
@admin_required
def delete_question(id):
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

