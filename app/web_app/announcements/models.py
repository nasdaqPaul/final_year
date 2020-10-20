import datetime

from app import db


class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    sender_id = db.Column(db.String(64), db.ForeignKey('staffs.staff_id'), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    ref_number = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Announcement: {self.title}>"
