from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ActivityForm(FlaskForm):
    activity_name = StringField("Activity Name", [DataRequired()])
    venue = StringField("Venue", [DataRequired()])
    description = TextAreaField("Description")
    date = StringField('Date')
    start_time = StringField('Starts at', [DataRequired()])
    end_time = StringField("End at", [DataRequired()])

    submit = SubmitField("Create Event")
