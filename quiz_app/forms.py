
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField, TextAreaField, FieldList, FormField, RadioField, SelectMultipleField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

user_length = 2
pass_length = 1

form_control = {"class": "form-control"}
form_check_input = {"class" : "form-check-input"}
form_check_label = {"class" : "form-check-label"}

class UserTypeForm(FlaskForm):
    usertype = SelectField('User Type', choices=[('admin', 'Admin'), ('user', 'User')], default='user')
    submit = SubmitField('select')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    is_admin = BooleanField('Is admin', default=False)
    username = StringField('Username', validators=[DataRequired(), Length(min=user_length, max=20)])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=pass_length, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField(label='First name', validators=[DataRequired()])
    last_name = StringField(label='Last name', validators=[DataRequired()])
    submit = SubmitField('Register')

# class AnswerForm(FlaskForm):
    # answer = StringField('Answer')
    # correct = BooleanField('Correct')

class QuizForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    question = TextAreaField('Question', validators=[DataRequired()])
    # answers = FieldList(FormField(AnswerForm), min_entries=4)

    answer1 = StringField('Answer')
    correct1 = BooleanField('Correct')
    answer2 = StringField('Answer')
    correct2 = BooleanField('Correct')
    answer3 = StringField('Answer')
    correct3 = BooleanField('Correct')
    answer4 = StringField('Answer')
    correct4 = BooleanField('Correct')

    active = BooleanField('Active', validators=[DataRequired()])
    category = StringField('Category')
    submit = SubmitField('Submit question')

class RadioForm(FlaskForm):
    # answers = RadioField('Label', choices=[('value1', 'Label1'), ('value2', 'Label2'), ('value3', 'Label3'), ('value4', 'Label4')])
    answer = RadioField(label='hello', choices = [], validators=[DataRequired()])
    submit = SubmitField('Submit')

class SelectForm(FlaskForm):
    answer = SelectMultipleField('Answer', choices=[('value1', 'Label1'), ('value2', 'Label2'), ('value3', 'Label3'), ('value4', 'Label4')])
    submit = SubmitField('Submit')

class TestTestForm(FlaskForm):
    answer = StringField('Answer')


class TestForm(FlaskForm):
    answers = FieldList(FormField(TestTestForm), min_entries=5)
    submit = SubmitField('Submit question')
