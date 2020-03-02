from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from wtforms.fields.html5 import DateTimeLocalField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    login = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

class AnnouncementForm(FlaskForm):
    title = StringField("Title", [DataRequired()])
    content = TextAreaField("Content", [DataRequired()],)
    recipients = BooleanField("Recipients", [DataRequired()])
    submit = SubmitField("Send")

class EventForm(FlaskForm):
    event_name = StringField("Event Name", [DataRequired()])
    venue = StringField("Venue", [DataRequired()])
    description = TextAreaField("Event Description")
    start_time = DateTimeField("Starts at", format="'%Y-%m-%d %H:%M:%S'")
    end_time = DateTimeField("End at", format="'%Y-%m-%d %H:%M:%S'")
    submit = SubmitField("Create Event")