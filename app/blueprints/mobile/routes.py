from flask import Blueprint, request, jsonify
from app.blueprints.mobile.models import Student, StudentAccount, AppInstance
from app.blueprints.web_app.models import Announcement
from app import db

mobile = Blueprint('mobile', __name__)


@mobile.route('/validate_student', methods=['POST'])
def login_student():

    adm_number = request.form.get('adm_number')
    password = request.form.get('password')

    # print('Adm Number: ' + adm_number + ' Password: ' + password): DEBUG

    student = Student.query.filter_by(adm_number=adm_number).first()
    # print(student): DEBUG
    if (student == None):
        return '3'

    elif (student.account == None):
        return '2'

    elif (student.account.check_password(password)):
        return '0'

    else:
        return '1'


@mobile.route("/register_student/<adm_number>/<token>")
def register_student(adm_number, token):
    # print('Adm Number: ' + adm_number + "| Token: " + token): DEBUG
    student = Student.query.get(adm_number)
    app_instance = AppInstance.query.get(adm_number)

    if app_instance == None:
        app_instance = AppInstance(adm_number=adm_number, token=token)
    else:
        app_instance.token = token

    db.session.add(app_instance)
    db.session.commit()

    return jsonify({
        "first_name": student.first_name,
        "last_name": student.last_name
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
