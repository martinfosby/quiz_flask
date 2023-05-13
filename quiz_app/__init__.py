#!/usr/bin/python
import sys
import logging
import flask
from flask_wtf.csrf import CSRFProtect

logging.basicConfig(stream=sys.stderr)
logging.basicConfig(filename="app.log", level=logging.DEBUG)

sys.path.insert(0,"/stud/mfo054/public_html/flask_app/")
sys.path.insert(1,"/stud/mfo054/public_html/flask_app/flask_app/")

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = 'my_secret_key'
csrf = CSRFProtect(app)


