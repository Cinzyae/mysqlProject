from flask import render_template
from flask_login import login_required

from app.main import main, cursor


@main.route('/show_file', methods=['POST', 'GET'])
@login_required
def show_file():
    cursor.execute('select * from coursefilemanagement.file')
    file_list = cursor.fetchall()
    print(file_list)
    return render_template('showfile.html', file_list=file_list)