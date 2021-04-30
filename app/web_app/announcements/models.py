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
    downloads = db.Column(db.Integer, nullable=False, default=0)

    @property
    def formatted_date(self):
        return self.date_posted.strftime("%b %d %Y at %I:%M %p")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Announcement: {self.title}>"
