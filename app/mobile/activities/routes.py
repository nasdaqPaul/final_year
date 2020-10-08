from flask import Blueprint
from app.web_app.activities.models import Activity

mobile = Blueprint('mobile_activities', __name__, url_prefix='/mobile/activities')


@mobile.route('/get/<activity_id>')
def get_activity(activity_id):
    announcement = Activity.query.get(activity_id)

    if announcement:
        pass
    else:
        pass
