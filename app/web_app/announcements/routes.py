import datetime

from flask import Blueprint, render_template, redirect, session, url_for, request, jsonify, flash
from flask_login import login_required, current_user

from app.google_fcm.messaging import send_announcement
from .forms import AnnouncementForm
from .models import Announcement
from ..auth.models import PermittedCourse
from ... import db
from ...mobile.auth.models import Student

web_announcements = Blueprint('web_announcements', __name__, template_folder='templates', static_folder='static',
                              url_prefix='/web/announcements')


# TODO: Reuse a couple of routes if you can
@web_announcements.route('/')
@login_required
def home():
    return render_template('web_app/announcements/index.html')


@web_announcements.route('/get_students')
@login_required
def get_students():
    course_code = request.args['course_code']
    permitted_course = PermittedCourse.query.filter_by(staff_id=current_user.staff_id, course_code=course_code).first()
    students = Student.query.filter_by(course_code=course_code).all()  # List of students
    student_js = []
    for student in students:
        student_js.append({
            'name': f"{student.first_name} {student.middle_name} {student.last_name}",
            'adm_number': f"{student.course_code}-{student.number}-{student.admission_year}"
        })
    return jsonify(student_js)


@web_announcements.route('/create')
@login_required
def create():
    if 'announcement_form' in session:
        form = AnnouncementForm()
        saved_announcement = session['announcement_form']
        form.title.data = saved_announcement['title']
        form.content.data = saved_announcement['content']
    else:
        form = AnnouncementForm()
    return render_template('web_app/announcements/create.html', form=form)


@web_announcements.route('/save/<next_link>', methods=['POST'])
@login_required
def save(next_link):
    form = AnnouncementForm()
    if form.validate_on_submit():
        session['announcement_form'] = {
            'title': form.title.data,
            'content': form.content.data
        }
    return redirect(url_for(next_link))


@web_announcements.route('/recipients')
@login_required
def recipients():
    permitted_courses = PermittedCourse.query.filter_by(staff_id=current_user.staff_id)
    return render_template('web_app/announcements/recipients.html', permitted_courses=permitted_courses)


@web_announcements.route('/preview')
@login_required
def preview():
    return render_template('web_app/announcements/preview.html')


@web_announcements.route('/save_recipients', methods=['POST'])
@login_required
def save_recipients():
    recipients = request.get_json()
    session['announcement_recipients'] = recipients
    return jsonify('success')


@web_announcements.route('/post')
@login_required
def post():
    now = datetime.datetime.now()
    custom_students = session.get('announcement_recipients').get('custom_students')
    express = session.get('announcement_recipients').get('express')

    new_announcement = Announcement(title=session['announcement_form']['title'],
                                    content=session['announcement_form']['content'], sender_id=current_user.staff_id,
                                    ref_number="test_ref")
    db.session.add(new_announcement)
    db.session.commit()

    db.session.refresh(new_announcement)

    for course_code, years in express.items():
        for year in years:
            students = Student.query.filter_by(course_code=course_code, admission_year=int(now.year) - int(year)).all()
            for student in students:
                if student.account:
                    if student.account.app:
                        send_announcement(student.account.app.token, new_announcement.id)
                custom_students.append(f"{student.course_code}-{student.number}-{student.admission_year}")
    print(custom_students)
    session.pop('announcement_form')
    session.pop('announcement_recipients')
    flash("Announcement Sent")
    return redirect(url_for('web_announcements.home'))
