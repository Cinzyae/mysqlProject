from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app.main import main, cursor


@main.route('/', methods=['GET'])
def show():
    if current_user.get_id() is None:
        return redirect(url_for('.login'))
    else:
        return render_template('homepage.html', userid=current_user.get_id())


@main.route('/homepage', methods=['POST', 'GET'])
@login_required
def homepage():
    title = 'unknown'
    if current_user.utype == 1:
        title = 'student'
    elif current_user.utype == 2:
        title = 'teacher'
    return render_template('homepage.html', userid=current_user.get_id(), title=title)
