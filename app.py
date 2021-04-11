import os
import random
from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask import request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

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
    if current_user.get_id() is None:
        return redirect(url_for('login'))
    else:
        return render_template('homepage.html', userid=current_user.get_id())


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
    return redirect(url_for('login'))


@app.route('/show_file', methods=['POST', 'GET'])
@login_required
def show_file():
    cursor.execute('select * from coursefilemanagement.file')
    file_list = cursor.fetchall()
    print(file_list)
    return render_template('showfile.html', file_list=file_list)


@app.route('/upload_file', methods=['POST', 'GET'])
@login_required
def upload_file():
    if request.method == 'GET':
        return render_template('upload_file.html')
    else:
        f = request.files['file']
        filename = secure_filename(f.filename)
        if os.path.exists('files'):
            print('base folder exists')
        else:
            os.mkdir('files')
        filepath = 'files/' + current_user.get_id()
        if os.path.exists(filepath):
            print('filepath exists')
        else:
            os.mkdir(filepath)
        f.save(os.path.join(filepath, filename))
        print(current_user.get_id())
        cursor.execute('insert into coursefilemanagement.file(fileName, fileID, account) values (%s,%s,%s)',
                       (filename, random.randint(1, 999999999), current_user.get_id()))
        conn.commit()
        return 'file uploaded successfully'


@app.route('/download_file', methods=['POST', 'GET'])
@login_required
def download_file():
    filepath = 'files/' + current_user.get_id()
    fileID = request.form['id']
    cursor.execute('select fileName from coursefilemanagement.file where fileID=%s', fileID)
    filename = cursor.fetchall()
    print(filepath)
    print(filename[0][0])
    return send_from_directory(filepath, filename[0][0], as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
