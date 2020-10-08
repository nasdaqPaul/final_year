from flask import Blueprint, render_template, redirect, session, url_for, request, jsonify
from flask_login import login_required, current_user
from .forms import AnnouncementForm
from ..auth.models import PermittedCourse
from ...mobile.auth.models import Student

web_announcements = Blueprint('web_announcements', __name__, template_folder='templates', static_folder='static',
                              url_prefix='/web/announcements')


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
    return render_template('preview.html')
