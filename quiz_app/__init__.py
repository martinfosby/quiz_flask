from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .users import users
from .quizes import quizes

app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(quizes)

app.config['SECRET_KEY'] = 'my_secret_key'
csrf = CSRFProtect(app)


