from app import db
from werkzeug.security import check_password_hash, generate_password_hash


class Student(db.Model):
    __tablename__ = "students"

    course_code = db.Column(db.CHAR(3), db.ForeignKey("courses.course_code"), primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    admission_year = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(64), nullable=False)
    middle_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    account = db.relationship('StudentAccount', uselist=False, back_populates='owner')

    def __repr__(self):
        return "<Student: %s %s>" % (self.first_name, self.last_name)


class StudentAccount(db.Model):
    __tablename__ = 'student_accounts'

    course_code = db.Column(db.CHAR(3), primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    admission_year = db.Column(db.Integer, primary_key=True)

    db.ForeignKeyConstraint([course_code, number, admission_year],
                            [Student.course_code, Student.number, Student.admission_year])

    owner = db.relationship('Student', back_populates = 'account', uselist=False)
    app = db.relationship('AppInstance', back_populates='account', uselist=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class AppInstance(db.Model):
    __tablename__ = 'app_instances'

    course_code = db.Column(db.CHAR(3), primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    admission_year = db.Column(db.Integer, primary_key=True)

    db.ForeignKeyConstraint([course_code, number, admission_year], [StudentAccount.course_code, StudentAccount.number, StudentAccount.admission_year])

    token = db.Column(db.String(240), nullable=False)
    account = db.relationship('StudentAccount', back_populates='app', uselist=False)

    def updateToken(self, token):
        self.token = token
        db.session.commit()