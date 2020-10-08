from app import db
import datetime

class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    sender_id = db.Column(db.String(64), db.ForeignKey('staffs.staff_id'), nullable=False)
    posted_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Announcement: {self.title}>"
