from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo



class AnnouncementForm(FlaskForm):
    title = StringField("Title", [DataRequired()])
    content = TextAreaField("Content", [DataRequired()])
    submit = SubmitField("Send")


class EventForm(FlaskForm):
    event_name = StringField("Event Name", [DataRequired()])
    venue = StringField("Venue", [DataRequired()])
    description = TextAreaField("Event Description")
    date = StringField('Date')
    start_time = StringField('Starts at', [DataRequired()])
    end_time = StringField("End at", [DataRequired()])

    submit = SubmitField("Create Event")
