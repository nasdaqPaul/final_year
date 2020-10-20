import datetime

from app import db


class Activity(db.Model):
    __tablename__ = "activities"
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(64), nullable=False)
    activity_description = db.Column(db.Text(), nullable=False)
    venue = db.Column(db.String(64), nullable=False)
    creator_id = db.Column(db.String(64), db.ForeignKey('staffs.staff_id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    end_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __str__(self):
        return self.event_name

    def __repr__(self):
        return f"<Event: {self.event_name}>"
