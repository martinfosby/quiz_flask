#!/usr/bin/python
import sys
import logging
activate_this = '/stud/feide_alias/public_html/flask_app/flask_app/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/stud/mfo054/public_html/flask_app/")
sys.path.insert(1,"/stud/mfo054/public_html/flask_app/flask_app/")

from flask_app import app as application
