from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AnnouncementForm(FlaskForm):
    title = StringField("Title", [DataRequired()])
    content = TextAreaField("Content", [DataRequired()])
    submit = SubmitField("Send")
