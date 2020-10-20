from flask import Blueprint, render_template, redirect, request, session, url_for, jsonify
from flask_login import login_required, current_user

from app.web_app.auth.models import PermittedCourse
from .forms import ActivityForm

web_activities = Blueprint('web_activities', __name__, template_folder='templates', static_folder='static',
                           url_prefix='/web/activities')


@web_activities.route('/')
@login_required
def home():
    return render_template('web_app/activities/index.html', title='Activities')


@web_activities.route('/create')
@login_required
def create():
    if 'activity_form' in session:
        form = ActivityForm()

        saved_activity = session['activity_form']
        form.activity_name.data = saved_activity['name']
        form.venue.data = saved_activity['venue']
        form.description.data = saved_activity['content']
        form.date.data = saved_activity['date']
        form.start_time.data = saved_activity['start_time']
        form.end_time.data = saved_activity['end_time']
    else:
        form = ActivityForm()
    return render_template('web_app/activities/create.html', form=form, title="Activities | Create")


@web_activities.route('/save/<next_link>', methods=['POST'])
def save(next_link):
    form = ActivityForm()

    if form.validate_on_submit():
        session['activity_form'] = {
            'name': form.activity_name.data,
            'venue': form.venue.data,
            'content': form.description.data,
            'date': form.date.data,
            'start_time': form.start_time.data,
            'end_time': form.end_time.data
        }
    return redirect(url_for(next_link))


@web_activities.route('/recipients')
@login_required
def recipients():
    recipients = PermittedCourse.query.filter_by(staff_id=current_user.staff_id)
    return render_template('web_app/activities/recipients.html', permitted_courses=recipients)


@web_activities.route('/save_recipients', methods=['POST'])
@login_required
def save_recipients():
    recipients = request.get_json()
    print(recipients)
    return jsonify('success')


@web_activities.route('/preview')
@login_required
def preview():
    return render_template('/web_app/activities/preview.html')
