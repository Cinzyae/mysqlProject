import random
import time

from flask import render_template, request
from flask_login import login_required, current_user

from app.main import main, cursor, conn


@main.route('/mailbox', methods=['POST', 'GET'])
@login_required
def mailbox():
    if current_user.utype == 1:
        cursor.execute('select tid, sid, messageid, content, direction '
                       'from coursefilemanagement.message natural join coursefilemanagement.student '
                       'where account = %s',
                       (current_user.get_id()))
        message_list = cursor.fetchall()
        print(message_list)
        return render_template('mailbox.html', message_list=message_list)
    elif current_user.utype == 2:
        cursor.execute('select tid, sid, messageid, content, direction '
                       'from coursefilemanagement.message natural join coursefilemanagement.teacher '
                       'where account = %s',
                       (current_user.get_id()))
        message_list = cursor.fetchall()
        print(message_list)
        return render_template('mailbox.html', message_list=message_list)


@main.route('/newmessage', methods=['POST', 'GET'])
@login_required
def newmessage():
    if request.method == 'GET':
        return render_template('mailbox.html')
    else:
        receiver = request.form['receiver']
        content = request.form['content']
        if current_user.utype == 1:
            cursor.execute('select sID '
                           'from coursefilemanagement.student '
                           'where account=%s', (current_user.get_id()))
            sid = cursor.fetchall()
            messageID = time.strftime("%m%d%H%M%S", time.localtime()) + str(random.randint(1, 99))
            cursor.execute('insert into coursefilemanagement.message(sID, tID, messageID, content, direction) '
                           'values (%s,%s,%s,%s,%s)',
                           (sid[0][0], receiver, messageID, content, 0))
            conn.commit()
            return 'success!'
        elif current_user.utype == 2:
            cursor.execute('select tID '
                           'from coursefilemanagement.teacher '
                           'where account=%s', (current_user.get_id()))
            tid = cursor.fetchall()
            messageID = time.strftime("%m%d%H%M%S", time.localtime()) + str(random.randint(1, 99))
            cursor.execute('insert into coursefilemanagement.message(sID, tID, messageID, content, direction) '
                           'values (%s,%s,%s,%s,%s)',
                           (receiver, tid[0][0], messageID, content, 1))
            conn.commit()
            return 'success!'
