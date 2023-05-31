from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from quiz_app.forms import *

from ..db import *
from ..utils import *

user_has_answer = Blueprint('user_has_answer', __name__, url_prefix='/user_has_answer')


@user_has_answer.route('/', methods=['POST', 'GET'])
def home():
    user_answers = db_query_rows('SELECT * FROM user_has_answer')
    return render_template('user_has_answer/home.html')