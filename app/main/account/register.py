from flask import request, render_template

from app.main import main, cursor, conn


@main.route('/register', methods=['POST', 'GET'])  # 表单提交
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
