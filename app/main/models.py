from flask_login import UserMixin


class User(UserMixin):
    def __init__(self):
        self.type = 0

    def get_type(self):
        return self.type

    pass
