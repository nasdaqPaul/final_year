from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from app.web_app.models import Department


@login_manager.user_loader
def user_loader(user_id):
    return Staff.query.get(user_id)


class Staff(db.Model, UserMixin):
    __tablename__ = 'staffs'

    staff_id = db.Column(db.String(64), primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    school_code = db.Column(db.CHAR(3), nullable=False)
    department_code = db.Column(db.CHAR(3), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    db.ForeignKeyConstraint([department_code, school_code], [Department.department_code, Department.school_code])
    account = db.relationship('StaffAccount', uselist=False, back_populates='owner')
    announcements = db.relationship('Announcement', backref='sender', lazy=True)
    events = db.relationship('Activity', backref='creator', lazy=True)

    def __str__(self):
        return self.first_name + self.first_name

    def __repr__(self):
        return f"<Staff: {self.first_name} {self.last_name}>"

    def get_id(self):
        return self.staff_id


class StaffAccount(db.Model):
    __tablename__ = 'staff_accounts'
    username = db.Column(db.String, db.ForeignKey('staffs.staff_id'), primary_key=True)
    password = db.Column(db.String(120), nullable=False)

    owner = db.relationship('Staff', back_populates='account', uselist=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __str__(self):
        return self.owner.first_name + self.owner.first_name

    def __repr__(self):
        return f"<StaffAccount => {self.owner.first_name} {self.owner.last_name}>"


class PermittedCourse(db.Model):
    __tablename__ = 'permitted_courses'

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(64), db.ForeignKey('staffs.staff_id'), nullable=False)
    course_code = db.Column(db.CHAR(3), db.ForeignKey('courses.course_code'), nullable=False)
    levels = db.Column(db.ARRAY(db.INTEGER))
