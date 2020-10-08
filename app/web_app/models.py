from app import db


class Department(db.Model):
    __tablename__ = 'departments'

    school_code = db.Column(db.CHAR(3), db.ForeignKey('schools.school_code'), primary_key=True)
    department_code = db.Column(db.CHAR(3), primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    courses = db.relationship('Course', backref='department', lazy=False)
    staffs = db.relationship('Staff', backref='department', lazy=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Department: {self.name}>"


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
    def courses(self):
        _courses = []
        for department in self.departments:
            for course in department.courses:
                _courses.append(course)

        return _courses

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<School: {self.name}>"


class Course(db.Model):
    __tablename__ = 'courses'

    course_code = db.Column(db.CHAR(3), primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    school_code = db.Column(db.CHAR(3), nullable=False)
    department_code = db.Column(db.CHAR(3), nullable=False)

    db.ForeignKeyConstraint([school_code, department_code], [Department.school_code, Department.department_code])
    students = db.relationship('Student', backref='course', lazy=False)
    permitted_senders = db.relationship('PermittedCourse', backref='course', lazy=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Course: {self.name}>"

# def initialize_database():
#     # Staffs
#     staff1 = Staff(first_name="Washington", last_name="Oluoch", school_code='004', department_code='001', role="HOD",
#                    staff_id="staff_001")
#     staff2 = Staff(first_name="Raphael", last_name="Kaibiru", school_code='004', department_code='001',
#                    role="Project Coordinator", staff_id="staff_002")
#     staff3 = Staff(first_name='John', last_name='Doe', school_code='004', department_code='002', role='Proj',
#                    staff_id='staff_003')
#     staff4 = Staff(first_name='Jane', last_name='Doe', school_code='004', department_code='002', role='Sec',
#                    staff_id='staff_004')
#
#     # Students
#     student1 = Student(course_code="J17", admission_year=2016, number=9030, first_name="Paul", last_name="Nasdaq",
#                        middle_name="Odhiambo")
#     student2 = Student(course_code="J77", number=9031, first_name="Silla", last_name="Montella",
#                        admission_year=2016, middle_name="Dienya")
#
#     # Schools, departments and courses
#     eng_tech = School(school_code='001', name="Engineering and Technology")
#
#     eng = Department(department_code='002', school_code='001', name='Engineering')
#     comp_science = Department(department_code='001', name="Computing", school_code='001')
#
#     elec = Course(course_code='J16', name='Elecrical Engineering', department_code='002')
#     mec = Course(course_code='J15', name='Mechanical Engineering', department_code='002')
#     it = Course(course_code='J77', name='Information Technology', department_code='001')
#     cs = Course(course_code='J17', name='Computer Science', department_code='001')
#
#     # Accounts
#     staff1_account = StaffAccount(username=staff1.staff_id)
#     staff1_account.set_password("1234")
#
#     staff2_account = StaffAccount(username=staff2.staff_id)
#     staff2_account.set_password("1234")
#
#     staff3_account = StaffAccount(username=staff3.staff_id)
#     staff3_account.set_password('1234')
#
#     staff4_account = StaffAccount(username=staff4.staff_id)
#     staff4_account.set_password('1234')
#
#     student1_account = StudentAccount(course_code=student1.course_code, number=student1.number,
#                                       admission_year=student1.admission_year)
#     student1_account.set_password("1234")
#
#     student2_account = StudentAccount(course_code=student2.course_code, number=student2.number,
#                                       admission_year=student2.admission_year)
#     student2_account.set_password("1234")
#
#     db.session.add_all(
#         [staff1, staff2, staff3, staff4, staff1_account, staff2_account, staff3_account, staff4_account])
#     db.session.commit()
