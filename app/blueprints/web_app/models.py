from app import db, login_manager
from app.blueprints.mobile.models import Student, StudentAccount
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime



@login_manager.user_loader
def user_loader(id):
    return Staff.query.get(id)


class Staff(db.Model, UserMixin):
    __tablename__ = 'staffs'


    staff_id = db.Column(db.String(64), primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    department_code = db.Column(db.CHAR(3), db.ForeignKey('departments.department_code'), nullable=False)
    school_code = db.Column(db.CHAR(3), db.ForeignKey('schools.school_code'), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    account = db.relationship('StaffAccount', uselist=False, back_populates='owner')
    announcements = db.relationship('Announcement', backref='sender', lazy=True)
    events = db.relationship('Event', backref='creator', lazy=True)

    def get_id(self):
        return self.staff_id


class StaffAccount(db.Model):
    __tablename__ = 'staff_accounts'
    username = db.Column(db.String, db.ForeignKey('staffs.staff_id'), primary_key=True)
    owner = db.relationship('Staff', back_populates='account', uselist=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    sender_id = db.Column(db.String(64), db.ForeignKey('staffs.staff_id'), nullable=False)
    posted_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(64), nullable=False)
    event_description = db.Column(db.Text(), nullable=False)
    venue = db.Column(db.String(64), nullable=False)
    creator_id = db.Column(db.String(64), db.ForeignKey('staffs.staff_id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    end_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class Department(db.Model):
    __tablename__ = 'departments'
    department_code = db.Column(db.CHAR(3), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    staffs = db.relationship('Staff', backref='department', lazy=False)

class School(db.Model):
    __tablename__ = 'schools'
    school_code = db.Column(db.CHAR(3), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    staffs = db.relationship('Staff', backref='school', lazy=False)

####


def initialize_database():
    # Staffs
    staff1 = Staff(first_name="Washington", last_name="Oluoch", level=1, department_code='001', school_code='001', role="HOD", staff_id="staff_001")
    staff2 = Staff(first_name="Raphael", last_name="Kaibiru", level=3, department_code='001', school_code='001', role="Project Coordinator", staff_id="staff_002")
    # Students
    student1 = Student(department="J17", admission_year=2016, number=9030, first_name="Paul", last_name="Nasdaq", middle_name="Odhiambo")
    student2 = Student(department="J77", number=9031, first_name="Silla", last_name="Montella", admission_year=2016, middle_name="Dienya")

    # Departments and schools
    eng_tech = School(school_code='001', name="Engineering and Technology")
    comp_science = Department(department_code='001', name="Computer Science")

    # Accounts
    staff1_account = StaffAccount(username=staff1.staff_id)
    staff1_account.set_password("1234")

    staff2_account = StaffAccount(username=staff2.staff_id)
    staff2_account.set_password("1234")

    student1_account = StudentAccount(adm_number=student1.adm_number)
    student1_account.set_password("1234")

    student2_account = StudentAccount(adm_number=student2.adm_number)
    student2_account.set_password("1234")

    db.session.add_all([staff1, staff2, student1, student2, staff1_account, student2_account, student1_account, student2_account, eng_tech, comp_science])
    db.session.commit()
