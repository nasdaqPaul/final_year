from app import db, login_manager
from app.blueprints.mobile.models import Student, StudentAccount
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def user_loader(user_id):
    return Staff.query.get(user_id)


class Staff(db.Model, UserMixin):
    __tablename__ = 'staffs'

    staff_id = db.Column(db.String(64), primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    department_code = db.Column(db.CHAR(3), db.ForeignKey('departments.department_code'), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    account = db.relationship('StaffAccount', uselist=False, back_populates='owner')
    announcements = db.relationship('Announcement', backref='sender', lazy=True)
    events = db.relationship('Event', backref='creator', lazy=True)

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


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(64), nullable=False)
    event_description = db.Column(db.Text(), nullable=False)
    venue = db.Column(db.String(64), nullable=False)
    creator_id = db.Column(db.String(64), db.ForeignKey('staffs.staff_id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    end_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __str__(self):
        return self.event_name

    def __repr__(self):
        return f"<Event: {self.event_name}>"


class Department(db.Model):
    __tablename__ = 'departments'

    department_code = db.Column(db.CHAR(3), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    school_code = db.Column(db.CHAR(3), db.ForeignKey('schools.school_code'), nullable=False)

    courses = db.relationship('Course', backref='department', lazy=False)
    staffs = db.relationship('Staff', backref='department', lazy=False)


    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Department: {self.name}>"


class Course(db.Model):
    __tablename__ = 'courses'

    course_code = db.Column(db.CHAR(3), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    department_code = db.Column(db.CHAR(3), db.ForeignKey('departments.department_code'), nullable=False)

    students = db.relationship('Student', backref='course', lazy=False)


class School(db.Model):
    __tablename__ = 'schools'

    school_code = db.Column(db.CHAR(3), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    departments = db.relationship('Department', backref='school', lazy=False)

    @property
    def staffs(self):
        _staffs = []
        for department in self.departments:
            for staff in department.staffs:
                _staffs.append(staff)

        return _staffs

    @property
    def students(self):
        _students = []
        for department in self.departments:
            for student in department.students:
                _students.append(student)

        return _students

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<School: {self.name}>"




def initialize_database():
    # Staffs

    staff1 = Staff(first_name="Washington", last_name="Oluoch", level=1, department_code='001', role="HOD",
                   staff_id="staff_001")
    staff2 = Staff(first_name="Raphael", last_name="Kaibiru", level=3, department_code='001',
                   role="Project Coordinator", staff_id="staff_002")

    # Students
    student1 = Student(course_code="J17", admission_year=2016, number=9030, first_name="Paul", last_name="Nasdaq",
                       middle_name="Odhiambo")
    student2 = Student(course_code="J77", number=9031, first_name="Silla", last_name="Montella",
                       admission_year=2016, middle_name="Dienya")

    # Schools, departments and courses
    eng_tech = School(school_code='001', name="Engineering and Technology")
    med = Department(department_code='002', school_code='001', name='Medicalsudo')
    comp_science = Department(department_code='001', name="Computing", school_code='001')
    it = Course(course_code='J16', name='Information Technology', department_code='001')
    cs = Course(course_code='J17', name='Computer Science', department_code='001')

    # Accounts
    staff1_account = StaffAccount(username=staff1.staff_id)
    staff1_account.set_password("1234")

    staff2_account = StaffAccount(username=staff2.staff_id)
    staff2_account.set_password("1234")

    student1_account = StudentAccount(course_code=student1.course_code, number=student1.number,
                                      admission_year=student1.admission_year)
    student1_account.set_password("1234")

    student2_account = StudentAccount(course_code=student2.course_code, number=student2.number,
                                      admission_year=student2.admission_year)
    student2_account.set_password("1234")

    db.session.add_all([eng_tech, med, comp_science, staff1, staff2, student1, student2, staff1_account, staff2_account,
                        student1_account, student2_account])
    db.session.commit()
