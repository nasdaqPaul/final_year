from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import logout_user, login_required, login_user
from werkzeug.urls import url_parse

from app import db
from app import login_manager
from .forms import LoginForm, RegistrationForm
from .models import StaffAccount, Staff

login_manager.login_view = "web_auth.login"
web_auth = Blueprint('web_auth', __name__, template_folder='templates', static_folder='static', url_prefix='/web/auth')


@web_auth.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        staff = Staff.query.get(login_form.username.data)
        if staff is None:
            flash("User with that ID does not exist in the database, please contact Admin for help")
            return render_template('web_app/auth/login.html', form=login_form, title='Log in')

        elif staff.account is None:
            flash("User does not have an account, register to proceed")
            return redirect(url_for('web_auth.register'))

        elif staff.account.check_password(login_form.password.data):
            login_user(staff)
            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('web_main.home')
            flash("Welcome")
            return redirect(next_page)

        else:
            flash("Wrong username or password")
            return render_template('web_app/auth/login.html', form=login_form, title='Login')

    return render_template('web_app/auth/login.html', form=login_form, title='Log in')


@web_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web_main.home'))


@web_auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Staff.query.get(form.username.data)

        if user is None:
            flash("The user does not exist")
            return render_template('web_app/auth/register.html', form=form)

        elif user.account:
            flash("The user already has an account")
            return render_template('web_app/auth/register.html', form=form, message='User already has an account')

        else:
            account = StaffAccount(username=form.username.data)
            account.set_password(form.password.data)
            db.session.add(account)
            db.session.commit()
            flash("Registration successfull!!")
            return redirect(url_for('web_auth.login'))

    return render_template('web_app/auth/register.html', message=None, title='Register', form=form)
