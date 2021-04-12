from flask import request, send_from_directory
from flask_login import login_required, current_user

from app.main import cursor, main


@main.route('/download_file', methods=['POST', 'GET'])
@login_required
def download_file():
    filepath = '../'+'files/' + current_user.get_id()
    fileID = request.form['id']
    cursor.execute('select fileName from coursefilemanagement.file where fileID=%s', fileID)
    filename = cursor.fetchall()
    print(filepath)
    print(filename[0][0])
    return send_from_directory(filepath, filename[0][0], as_attachment=True)
