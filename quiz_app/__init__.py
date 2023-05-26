from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .users import users
from .quizes import quizes
from .questions import questions
from .answers import answers
from quiz_app.utils import get_user

app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(questions)
app.register_blueprint(quizes)
app.register_blueprint(answers)

app.config['SECRET_KEY'] = 'my_secret_key'
csrf = CSRFProtect(app)


# Define the context processor
@app.context_processor
def inject_variables():
    # Determine if the user is an administrator
    is_admin = False
    if user := get_user():
        is_admin = user.get('is_admin')
    
    # Define the variables to be available in all templates
    return dict(is_admin=is_admin)
