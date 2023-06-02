from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from quiz_app.forms import *

from ..db import *
from ..utils import *

user_has_question = Blueprint('user_has_question', __name__, url_prefix='/user_has_question')


@user_has_question.route('/', methods=['POST', 'GET'])
@admin_required
def home():
    user_answers = db_query_rows('SELECT * FROM user_has_answer')
    return render_template('user_has_answer/home.html', user_answers=user_answers)