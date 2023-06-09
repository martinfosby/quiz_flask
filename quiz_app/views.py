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
from .utils import *
import werkzeug
import random
import uuid
# app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(days=7)



# dbconfig = {
#         'host': 'localhost',
#         'user': 'root',
#         'password': 'test',
#         'database': 'quiz_web_app',
#     }



@app.route('/home')
@app.route('/', methods=['POST', 'GET'])
def home():
    if session.get('id'):
        user = get_user_by_id(session.get('id'))
        if user.get('is_admin'):
            return render_template('home.html')
        else:
            return redirect(url_for('quizes.home'))
    else:
        return redirect(url_for('users.login_user_type'))



@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")