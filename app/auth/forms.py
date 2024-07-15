from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired
from . import auth


class Login(FlaskForm):
    name = StringField('Eneter user name', validators=[DataRequired()])
    password = PasswordField('Enter password', validators=[DataRequired()])
    submit = SubmitField("Login")

class Register(FlaskForm):
    name = StringField('Enter user name', validators=[DataRequired()])
    email = StringField('Enter user email address', validators=[DataRequired(), Email(message='Please enter a valid email address!')])
    password = PasswordField('Enter password', validators=[InputRequired(message=''), Length(min=7, message='The minimum length is 7 characters!')])
    password_2 = PasswordField('Enter password again', validators=[DataRequired(), EqualTo('password', message='Passwords must be identical!')])
    submit = SubmitField("Registry")

class PasswordChange(FlaskForm):
    old_password = PasswordField('Enter password', validators=[InputRequired(message=''), Length(min=7, message='The minimum length is 7 characters!')])
    password = PasswordField('Enter new password', validators=[InputRequired(message=''), Length(min=7, message='The minimum length is 7 characters!')])
    password_2 = PasswordField('Enter new password again', validators=[DataRequired(), EqualTo('password', message='Passwords must be identical!')])
    submit = SubmitField("Change password")

class UserEdit(FlaskForm):
    id = IntegerField()
    name = StringField('Enter user name', validators=[DataRequired()])
    email = StringField('Enter user email address', validators=[DataRequired(), Email(message='Please enter a valid email address!')])
    role = SelectField('Role of the user', choices=[('user', 'user'), ('admin', 'admin')])
    password = PasswordField('Enter password', validators=[ Length(min=7, message='The minimum length is 7 characters!')])
    password_2 = PasswordField('Enter password again', validators=[EqualTo('password', message='Passwords must be identical!')])
    submit = SubmitField("Change data")