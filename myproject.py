from flask import url_for, render_template
from flask_login import LoginManager, current_user
from werkzeug.utils import redirect

from app import create_app
from app.main.models import User

app = create_app()

login_manager = LoginManager()
login_manager.login_view = '.login'
login_manager.login_message_category = 'info'
login_manager.login_message = '请登录'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    curr_user = User()
    curr_user.id = user_id
    return curr_user


@app.route('/', methods=['GET'])
def show():
    if current_user.get_id() is None:
        return redirect(url_for('main.login'))
    else:
        return render_template('homepage.html', userid=current_user.get_id())


if __name__ == '__main__':
    app.run()
