from flask import url_for
from flask_login import login_required, logout_user
from werkzeug.utils import redirect

from app.main import main


@main.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))
