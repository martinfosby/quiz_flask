#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/stud/mfo054/public_html/flask_app/")
sys.path.insert(1,"/stud/mfo054/public_html/flask_app/flask_app/")

from flask_app import app as application
