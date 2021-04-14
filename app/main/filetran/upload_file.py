import os
import random
import time

from flask import request, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.main import cursor, conn, main


@main.route('/upload_file', methods=['POST', 'GET'])
@login_required
def upload_file():
    if request.method == 'GET':
        return render_template('uploadfile.html')
    else:
        f = request.files['file']
        filename = secure_filename(f.filename)
        if os.path.exists('../files'):
            print('base folder exists')
        else:
            os.mkdir('../files')
        filepath = 'files/' + current_user.get_id()
        if os.path.exists(filepath):
            print('filepath exists')
        else:
            os.mkdir(filepath)
        f.save(os.path.join(filepath, filename))
        print(current_user.get_id())
        fileID = time.strftime("%m%d%H%M%S", time.localtime()) + str(random.randint(1, 99))
        cursor.execute('insert into coursefilemanagement.file(fileName, fileID, account) values (%s,%s,%s)',
                       (filename, fileID, current_user.get_id()))
        conn.commit()
        return render_template('uploadfile.html')
