from flask_login import LoginManager

from app import create_app
from app.main.models import User

app = create_app()

login_manager = LoginManager()
login_manager.login_view = '.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'please login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    curr_user = User()
    curr_user.id = user_id
    return curr_user


if __name__ == '__main__':
    app.run()
