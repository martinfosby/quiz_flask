from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .users import users
from .quizes import quizes
from .questions import questions

app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(questions)
app.register_blueprint(quizes)

app.config['SECRET_KEY'] = 'my_secret_key'
csrf = CSRFProtect(app)


