from flask import Blueprint
from app.web_app.announcements.models import Announcement

mobile = Blueprint('mobile_announcements', __name__, url_prefix='/mobile/announcements')


@mobile.route('/get/<announcement_id>')
def get_announement(announcement_id):
    announcement = Announcement.query.get(announcement_id)

    if announcement:
        pass
    else:
        pass
