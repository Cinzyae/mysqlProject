import random
import time

from flask import render_template, request
from flask_login import login_required, current_user

from app.main import main, cursor, conn


@main.route('/mailbox', methods=['POST', 'GET'])
@login_required
def mailbox():
    cursor.execute('select usertype '
                   'from coursefilemanagement.user '
                   'where account=%s', (current_user.get_id()))
    detail = cursor.fetchall()
    ac_type = detail[0][0]
    if ac_type == 1:
        cursor.execute('select * '
                       'from coursefilemanagement.message natural join coursefilemanagement.student '
                       'where account = %s',
                       (current_user.get_id()))
        message_list = cursor.fetchall()
        print(message_list)
        return render_template('mailbox.html', message_list=message_list)
    elif ac_type == 2:
        cursor.execute('select * '
                       'from coursefilemanagement.message natural join coursefilemanagement.teacher '
                       'where account = %s',
                       (current_user.get_id()))
        message_list = cursor.fetchall()
        print(message_list)
        return render_template('mailbox.html', message_list=message_list)
    # TODO : table head


@main.route('/newmessage', methods=['POST', 'GET'])
@login_required
def newmessage():
    if request.method == 'GET':
        return render_template('mailbox.html')
    else:
        receiver = request.form['receiver']
        content = request.form['content']
        cursor.execute('select usertype '
                       'from coursefilemanagement.user '
                       'where account=%s', (current_user.get_id()))
        detail = cursor.fetchall()
        ac_type = detail[0][0]
        if ac_type == 1:
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

        # TODO : configure sID or tID
