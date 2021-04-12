from flask import request, render_template, redirect, url_for
from flask_login import login_user

from app.main import main, cursor
from app.main.models import User


@main.route('/login', methods=['POST', 'GET'])
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
                    return redirect(url_for('.homepage'))

        return '<h>账号、密码错误！</h>'
