from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from quiz_app.forms import *

from ..db import *
from ..utils import *

user_has_answer = Blueprint('user_has_answer', __name__, url_prefix='/user_has_answer')


@user_has_answer.route('/', methods=['POST', 'GET'])
@admin_required
def home():
    users_answers = db_query_rows('SELECT * FROM user_has_answer')
    return render_template('user_has_answer/home.html', users_answers=users_answers)

# @user_has_answer.route('/read', methods=['POST', 'GET'])
# @admin_required
# def read():
#     quizes = db_query_rows('SELECT answer_question_quiz_id FROM user_has_answer GROUP BY answer_question_quiz_id')
#     questions = db_query_rows('SELECT * FROM `user_has_answer` GROUP BY answer_question_id;')
#     users_answers = db_query_rows('SELECT * FROM user_has_answer')

#     quizes_dict = {}
#     for question in questions:
#         quizes_dict[question['answer_question_quiz_id']] = {'questions': [question]}

#     # for quiz in quizes:
#     #     quiz['questions'] = []
#     #     for question in questions:
#     #         if quiz['answer_question_quiz_id'] == question['answer_question_quiz_id']:
#     #             quiz['questions'].append(question)

#     return render_template('user_has_answer/read.html', users_answers=users_answers, quizes=quizes, questions=questions)