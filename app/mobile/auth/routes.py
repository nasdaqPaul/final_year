from flask import Blueprint, jsonify, request

from app import db
from .models import Student, AppInstance

mobile = Blueprint('mobile_auth', __name__, url_prefix='/mobile/auth')


@mobile.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()

    course_code = login_data.get("course_code").upper()
    number = login_data.get("number")
    admission_year = login_data.get("admission_year")

    # TODO: Remove in deployment, for testing purposes only
    #
    print(f"Admission number: {course_code}-{number}-{admission_year}")
    print(f"Password: {login_data.get('password')}")
    print(f"Device ID: {login_data.get('instance_token')}")

    student = Student.query.filter_by(course_code=course_code, number=number,
                                      admission_year=admission_year).first()
    if student is None:
        return jsonify({
            "login_success": False,
            "student_data": None,
            "fail_message": "StudentNotFound"
        })

    elif student.account is None:
        return jsonify({
            "login_success": False,
            "student_data": None,
            "fail_message": "StudentNotRegistered"
        })

    elif student.account.check_password(login_data.get("password")) is not True:
        return jsonify({
            "login_success": False,
            "student_data": None,
            "fail_message": "WrongPassword"
        })

    else:
        app_instance = AppInstance.query.filter_by(course_code=course_code, number=number,
                                                   admission_year=admission_year).first()
        if app_instance is None:
            app_instance = AppInstance(course_code=course_code, number=number, admission_year=admission_year,
                                       token=login_data.get("instance_token"))
        else:
            app_instance.token = login_data.get("instance_token")

        db.session.add(app_instance)
        db.session.commit()

        return jsonify({
            "login_success": True,
            "student_data": {
                "first_name": student.first_name,
                "middle_name": student.middle_name,
                "last_name": student.last_name,
            },
            "fail_message": None

        })


@mobile.route('/logout')
def logout():
    pass


@mobile.route('/update_token', methods=['POST'])
def update_token():
    pass
