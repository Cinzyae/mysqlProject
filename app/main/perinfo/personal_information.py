from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app.main import main, cursor, conn


@main.route('/perinfo', methods=['POST', 'GET'])
@login_required
def perinfo():
    cursor.execute('select usertype from coursefilemanagement.user where account=%s', (current_user.get_id()))
    detail = cursor.fetchall()
    ac_type = detail[0][0]
    if ac_type == 1:
        cursor.execute('select * from coursefilemanagement.student')
        teacher_detail = cursor.fetchall()
        return render_template('perinfo.html', u_detail=teacher_detail)
    elif ac_type == 2:
        cursor.execute('select * from coursefilemanagement.teacher')
        teacher_detail = cursor.fetchall()
        return render_template('perinfo.html', u_detail=teacher_detail)


@main.route('/modifyinfo', methods=['POST', 'GET'])
@login_required
def modifyinfo():
    cursor.execute('select usertype from coursefilemanagement.user where account=%s', (current_user.get_id()))
    detail = cursor.fetchall()
    ac_type = detail[0][0]
    if ac_type == 1:
        return render_template('smodify.html')
    elif ac_type == 2:
        return render_template('tmodify.html')


@main.route('/smodify', methods=['POST', 'GET'])
@login_required
def smodify():
    if request.method == 'GET':
        return render_template('smodify.html')
    else:
        studentName = request.form['studentName']
        sID = request.form['sID']
        majorID = request.form['majorID']

        cursor.execute(
            'insert into coursefilemanagement.student(studentName, sID, account, majorID) values (%s,%s,%s,%s)',
            (studentName, sID, current_user.get_id(), majorID))

        conn.commit()
        return redirect(url_for('.perinfo'))


@main.route('/tmodify', methods=['POST', 'GET'])
@login_required
def tmodify():
    if request.method == 'GET':
        return render_template('tmodify.html')
    else:
        teacherName = request.form['teacherName']
        tID = request.form['tID']

        cursor.execute(
            'insert into coursefilemanagement.teacher(teacherName, tID, account) values (%s,%s,%s)',
            (teacherName, tID, current_user.get_id()))

        conn.commit()
        return redirect(url_for('.perinfo'))
