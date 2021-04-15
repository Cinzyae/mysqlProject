from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app.main import main, cursor, conn


@main.route('/perinfo', methods=['POST', 'GET'])
@login_required
def perinfo():
    if current_user.utype == 1:
        cursor.execute('select * from coursefilemanagement.student')
        student_details = cursor.fetchall()
        for student_detail in student_details:
            if student_detail[2] == current_user.get_id():
                return render_template('sperinfo.html', u_detail=(student_detail,))
        return render_template('sperinfo.html', u_detail=(('?', '?', '?', '?'),))

    elif current_user.utype == 2:
        cursor.execute('select * from coursefilemanagement.teacher')
        teacher_details = cursor.fetchall()
        cursor.execute('select * from coursefilemanagement.building')
        building_details = cursor.fetchall()
        cursor.execute('select * from coursefilemanagement.course')
        course_details = cursor.fetchall()
        cursor.execute('select * from coursefilemanagement.major')
        major_details = cursor.fetchall()
        cursor.execute('select * from coursefilemanagement.student_course')
        sc_details = cursor.fetchall()

        for teacher_detail in teacher_details:
            if teacher_detail[2] == current_user.get_id():
                return render_template('tperinfo.html', u_detail=(teacher_detail,), building_details=building_details,
                                       course_details=course_details, major_details=major_details,
                                       sc_details=sc_details)
        return render_template('tperinfo.html', u_detail=(('?', '?', '?'),), building_details=building_details,
                               course_details=course_details, major_details=major_details, sc_details=sc_details)


@main.route('/modifyinfo', methods=['POST', 'GET'])
@login_required
def modifyinfo():
    if current_user.utype == 1:
        return render_template('smodify.html')
    elif current_user.utype == 2:
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

        cursor.execute('DELETE FROM coursefilemanagement.student '
                       'WHERE account =%s', (current_user.get_id()))

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
        try:
            teacherName = request.form['teacherName']
            tID = request.form['tID']
            cursor.execute('DELETE FROM coursefilemanagement.teacher '
                           'WHERE account =%s', (current_user.get_id()))
            cursor.execute(
                'insert into coursefilemanagement.teacher(teacherName, tID, account) values (%s,%s,%s)',
                (teacherName, tID, current_user.get_id()))
        except:
            print('no teacher modified')

        try:
            buildingName = request.form['buildingName']
            buildingID = request.form['buildingID']
            cursor.execute('insert into coursefilemanagement.building(buildingName, buildingID) VALUES (%s,%s)',
                           (buildingName, buildingID))
        except:
            print('no building modified')

        try:
            courseName = request.form['courseName']
            courseID = request.form['courseID']
            tID = request.form['tID']
            buildingID = request.form['buildingID']
            cursor.execute('insert into coursefilemanagement.course VALUES (%s,%s,%s,%s)',
                           (courseName, courseID, tID, buildingID))
        except:
            print('no course modified')

        try:
            majorName = request.form['majorName']
            majorID = request.form['majorID']
            cursor.execute('insert into coursefilemanagement.major VALUES (%s,%s)',
                           (majorName, majorID))
        except:
            print('no major modified')

        try:
            courseID = request.form['courseID']
            sID = request.form['sID']
            cursor.execute('insert into coursefilemanagement.student_course VALUES (%s,%s)',
                           (courseID, sID))
        except:
            print('no course_student modified')

        conn.commit()
        return redirect(url_for('.perinfo'))
