from flask import Blueprint, request, render_template, redirect, flash, url_for
from app.blueprints.web_app.forms import LoginForm, RegistrationForm, AnnouncementForm, EventForm
from app.blueprints.web_app.models import Staff, StaffAccount, Announcement
from app.blueprints.mobile.models import AppInstance
from app import login_manager, db
from werkzeug.urls import url_parse
from flask_login import login_required, login_user, logout_user, current_user


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
            flash ("User with that ID does not exist in the database, please contact Admin for help")
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
            flash ("Wrong username or password")
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

@web.route('/createAnnouncement', methods=['POST', 'GET'])
@login_required
def createAnnouncement():
    form = AnnouncementForm()

    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, content=form.content.data, sender_id=current_user.get_id())
        db.session.add(announcement)
        db.session.commit()
        db.session.refresh(announcement)

        stds = AppInstance.query.all()
        tokens = []
        
        for instance in stds:
            tokens.append(instance.token)
        from app.google_fcm.messaging import send_multicast, send_to_token

        
        send_multicast(tokens=tokens, data= {
            "instruction" : "download_announcement",
            "message_id": str(announcement.id)
        })

        flash ("Message sent!!")
    return render_template('create_announcement.html', title="Create Announcement", form=form)

@web.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()

    return render_template('create_event.html', title="Create Event", form=form)