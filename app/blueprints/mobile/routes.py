from flask import Blueprint, request, jsonify
from app.blueprints.mobile.models import Student, StudentAccount, AppInstance
from app.blueprints.web_app.models import Announcement
from app import db

mobile = Blueprint('mobile', __name__)


@mobile.route('/login_student', methods=['POST'])
def login_student():
    login_data = request.get_json()
    department = login_data.get("department")

    try:
        number = int(login_data.get("number"))
        admission_year = int(login_data.get("admission_year"))

    except ValueError:
        print("Type Error")
        return jsonify({
            "Error": "WrongAdmFormat"
        })

    student = Student.query.filter_by(department=department, number=number, admission_year=admission_year).first()

    if student is None:
        return jsonify({
            "Error": "StudentNotFound"
        })
    elif student.account is None:
        return jsonify({
            "Error": "StudentNotRegistered"
        })
    elif student.account.check_password(login_data.get("password")) is not True:
        return jsonify({
            "Error": "WrongPassword"
        })
    else:
        app_instance = AppInstance.query.filter_by(department=department, number=number, admission_year=admission_year).first()
        if app_instance is None:
            app_instance = AppInstance(department=department, number=number, admission_year=admission_year, token=login_data.get("instance_token"))

        db.session.add(app_instance)
        db.session.commit()

        return jsonify({
            "Error": "None",
            "firstName": student.first_name,
            "lastName": student.last_name,
            "middleName": student.middle_name, # More data to send later, if needed by client mobile
        })


@mobile.route("/get_announcement/<message_id>")
def get_announcement(message_id):
    announcement = Announcement.query.get(message_id)

    if (announcement):

        value = jsonify({
            "from": "Dapartment of " + announcement.sender.department.name,
            "title": announcement.title,
            "content": announcement.content,
            "posted_on": announcement.posted_on
        })
        print("Value", value)
        return value
    else:
        return jsonify({
            "Error": "MessageNotFound",
            "message_id": message_id
        })


@mobile.route("/update_token/<adm_number>/<new_token>")
def update_token(adm_number, new_token):
    app_instance = AppInstance.query.get(adm_number)
    app_instance.token = new_token
    db.session.add(app_instance)
    db.session.commit()

    return "Success"
