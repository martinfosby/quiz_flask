
from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField, TextAreaField, FieldList, FormField, RadioField, SelectMultipleField, EmailField, widgets, validators, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo

user_length = 2
pass_length = 1

form_control = {"class": "form-control"}
form_check_input = {"class" : "form-check-input"}
form_check_label = {"class" : "form-check-label"}

def validate_multiple_select_field(form, field):
    if not field.data:
        raise validators.ValidationError('Please select at least one option.')

class UserTypeForm(FlaskForm):
    usertype = SelectField('User Type', choices=[('admin', 'Admin'), ('user', 'User'), ('guest', 'Guest')], default='user')
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
    first_name = StringField(label='First name')
    last_name = StringField(label='Last name')
    submit = SubmitField('Register')

class AnswerForm(FlaskForm):
    answer = StringField('Answer')
    submit = SubmitField('Submit answer')

class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Question', validators=[DataRequired()])
    answer_type = SelectField('Answer Type', choices=[('single', 'Single'), ('multiple', 'Multiple'), ('essay', 'Essay')], default='single', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Submit question')

class QuizForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    active = BooleanField('Active', validators=[DataRequired()], default=True)
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit quiz')

class CheckBoxForm(FlaskForm):
    answer = SelectMultipleField('Answer', choices=[], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Submit answer')

class RadioForm(FlaskForm):
    # answers = RadioField('Label', choices=[('value1', 'Label1'), ('value2', 'Label2'), ('value3', 'Label3'), ('value4', 'Label4')])
    answer = RadioField('Answer', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit answer')

class TextAreaForm(FlaskForm):
    id = HiddenField()
    text = TextAreaField()
    submit = SubmitField('Submit')

class TextForm(FlaskForm):
    id = HiddenField()
    text = TextAreaField()

class MultipleTextAreaForm(FlaskForm):
    answer = FieldList(FormField(TextForm), min_entries=0, validators=[DataRequired()])
    submit = SubmitField('Submit answer')



class SelectForm(FlaskForm):
    answer = SelectMultipleField('Answer', choices=[('value1', 'Label1'), ('value2', 'Label2'), ('value3', 'Label3'), ('value4', 'Label4')])
    submit = SubmitField('Submit')

class TestTestForm(FlaskForm):
    answer = StringField('Answer')


class TestForm(FlaskForm):
    answers = FieldList(FormField(TestTestForm), min_entries=5)
    submit = SubmitField('Submit question')
