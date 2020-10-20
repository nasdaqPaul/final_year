from flask import Blueprint, jsonify

from app.web_app.announcements.models import Announcement

mobile = Blueprint('mobile_announcements', __name__, url_prefix='/mobile/announcements')


@mobile.route('/get/<int:announcement_id>')
def get_announcement(announcement_id):
    announcement = Announcement.query.get(announcement_id)

    if announcement:
        return jsonify({
            "error": "None",
            "announcement": {
                "subject": announcement.title,
                "content": announcement.content,
                "ref_number": announcement.ref_number,
                "date_posted": announcement.date_posted
            },
            "sender": {
                "name": announcement.sender.first_name + announcement.sender.last_name,
                "department": announcement.sender.department.name
            }
        })
    else:
        return jsonify({
            "error": "NotFound"
        })
