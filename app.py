from flask import Flask, render_template, redirect, url_for
from flask import request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User
import pymysql

conn = pymysql.connect(user="root", password="hhh0425", database="coursefilemanagement")
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = '1234567'

login_manager = LoginManager()
login_manager.login_view = 'login'
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
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        usertype = request.form['usertype']
        account = request.form['account']
        password = request.form['password']
        if len(account) == 0 | len(password) == 0:
            return render_template('login.html')

        cursor.execute('select account from coursefilemanagement.user')
        accounts = cursor.fetchall()

        for account in accounts:
            if request.form['account'] == account[0]:
                cursor.execute('select password from coursefilemanagement.user where account=%s', (account[0]))
                pw = cursor.fetchall()

                if request.form['password'] == pw[0][0]:
                    curr_user = User()
                    curr_user.id = account[0]
                    login_user(curr_user)
                    return redirect(url_for('homepage'))

        return '<h>账号、密码错误！</h>'


@app.route('/register', methods=['POST', 'GET'])  # 表单提交
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        usertype = request.form['usertype']
        account = request.form['account']
        password = request.form['password']
        if len(account) == 0:
            return render_template('error.html')
        cursor.execute('insert into coursefilemanagement.user(usertype, account, password) values (%s,%s,%s)',
                       (usertype, account, password))

        conn.commit()
        return '<h>注册成功！请登录。</h><form action="/login" method="get"><p><button type="submit">返回登录</button></p></form>'


@app.route('/homepage', methods=['POST', 'GET'])
@login_required
def homepage():
    return render_template('homepage.html', userid=current_user.get_id())


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('show'))


@app.route('file', methods=['POST', 'GET'])
@login_required
def file():

    return render_template('file.html')


if __name__ == '__main__':
    app.run()
