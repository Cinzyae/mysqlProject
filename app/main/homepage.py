from flask import render_template
from flask_login import login_required, current_user

from app.main import main


@main.route('/homepage', methods=['POST', 'GET'])
@login_required
def homepage():
    return render_template('homepage.html', userid=current_user.get_id())
