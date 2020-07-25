from flask import Blueprint, request, render_template, redirect, flash, url_for, session, jsonify
from app.blueprints.web_app.forms import LoginForm, RegistrationForm, AnnouncementForm, EventForm
from app.blueprints.web_app.models import Staff, StaffAccount, Announcement, PermittedCourse
from app.blueprints.mobile.models import AppInstance
from app import login_manager, db
from werkzeug.urls import url_parse
from flask_login import login_required, login_user, logout_user, current_user
from app.blueprints.mobile.models import Student

web = Blueprint('web', __name__, template_folder='templates', static_folder='static', static_url_path='/web/static')
login_manager.login_view = 'web.login'


@web.route("/")
@login_required
def index():
    return render_template("index.html", title='Home')


@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))


@web.route("/login", methods=['POST', 'GET'])
def login():
    loginForm = LoginForm()

    if loginForm.validate_on_submit():
        staff = Staff.query.get(loginForm.username.data)
        if (staff == None):
            flash("User with that ID does not exist in the database, please contact Admin for help")
            return render_template('login.html', form=loginForm, title='Log in')
        elif (staff.account == None):
            flash("User does not have an account, register to proceed")
            return redirect('/register')
        elif (staff.account.check_password(loginForm.password.data)):
            login_user(staff)
            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('web.index')
            flash("Welcome")
            return redirect(next_page)
        else:
            flash("Wrong username or password")
            return render_template('login.html', form=loginForm, title='Login')
    return render_template('login.html', form=loginForm, title='Log in')


@web.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Staff.query.get(form.username.data)
        if (user == None):
            flash("The user does not exist")
            return render_template('register.html', form=form)
        elif (user.account != None):
            flash("The user already has an account")
            return render_template('register.html', form=form, message='User already has an account')
        else:
            account = StaffAccount(username=form.username.data)
            account.set_password(form.password.data)
            db.session.add(account)
            db.session.commit()
            flash("Registration successfull!!")
            return redirect('/login')

    return render_template('register.html', message=None, title='Register', form=form)


@web.route('/create_announcement', methods=['POST', 'GET'])
@login_required
def create_announcement():
    if 'announcement_form' in session:
        form = AnnouncementForm()
        saved_announcement = session['announcement_form']
        form.title.data = saved_announcement['title']
        form.content.data = saved_announcement['content']
    else:
        form = AnnouncementForm()
    return render_template('create_announcement.html', title="Create Announcement", form=form)


@web.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if 'event_form' in session:
        form = EventForm()
        saved_event = session['event_form']
        form.event_name.data = saved_event['name']
        form.venue.data = saved_event['venue']
        form.description.data = saved_event['content']
        form.date.data = saved_event['date']
        form.start_time.data = saved_event['start_time']
        form.end_time.data = saved_event['end_time']
    else:
        form = EventForm()
    return render_template('create_event.html', title="Create Event", form=form)


@web.route('/save_event/<next_link>', methods=['POST'])
@login_required
def save_event(next_link):
    # Gets called every time a user tries to leave the create event page and JS knows that the form has been modified
    form = EventForm()
    if form.validate_on_submit():
        session['event_form'] = {
            'name': form.event_name.data,
            'venue': form.venue.data,
            'content': form.description.data,
            'date': form.date.data,
            'start_time': form.start_time.data,
            'end_time': form.end_time.data
        }
    return redirect('/' + next_link)


@web.route('/save_announcement/<next_link>', methods=['POST'])
@login_required
def save_announcement(next_link):
    form = AnnouncementForm()
    if form.validate_on_submit():
        session['announcement_form'] = {
            'title': form.title.data,
            'content': form.content.data
        }
    return redirect('/' + next_link)


@web.route('/event_recipient')
@login_required
def event_recipient():
    recipients = PermittedCourse.query.filter_by(staff_id=current_user.staff_id)
    return render_template('recipients.html', permitted_courses=recipients)


@web.route('/announcement_recipient')
@login_required
def announcement_recipient():
    recipients = PermittedCourse.query.filter_by(staff_id=current_user.staff_id)
    return render_template('recipients_announcements.html', permitted_courses=recipients)


@web.route('/get_students')
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
