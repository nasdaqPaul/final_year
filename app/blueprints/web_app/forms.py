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


class Recipients:
    uni_first_year = BooleanField()
    uni_second_year = BooleanField()
    uni_third_year = BooleanField()
    uni_forth_year = BooleanField()

    sch_first_year = BooleanField()
    sch_second_year = BooleanField()
    sch_third_year = BooleanField()
    sch_forth_year = BooleanField()

    dpt_first_year = BooleanField()
    dpt_second_year = BooleanField()
    dpt_third_year = BooleanField()
    dpt_forth_year = BooleanField()


class AnnouncementForm(FlaskForm, Recipients):
    title = StringField("Title", [DataRequired()])
    content = TextAreaField("Content", [DataRequired()])
    submit = SubmitField("Send")
    # Recipients
    # school_all

class EventForm(FlaskForm):
    event_name = StringField("Event Name", [DataRequired()])
    venue = StringField("Venue", [DataRequired()])
    description = TextAreaField("Event Description")
    date = StringField('Date')
    start_time = StringField('Starts at', [DataRequired()])
    end_time = DateTimeField("End at", format="'%Y-%m-%d %H:%M:%S'")

    submit = SubmitField("Create Event")