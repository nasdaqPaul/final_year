from flask import Blueprint, render_template
from flask_login import login_required

web_main = Blueprint('web_main', __name__, template_folder='templates', static_folder='static', url_prefix='/web')


@web_main.route('/')
@login_required
def home():
    return render_template('web_app/main/index.html')
