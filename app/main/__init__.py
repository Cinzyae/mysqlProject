import pymysql
from flask import Blueprint

main = Blueprint('main', __name__)

conn = pymysql.connect(user="root", password="hhh0425", database="coursefilemanagement")
cursor = conn.cursor()

from .account import register, logout, login
from .filetran import show_file, download_file, upload_file
from .messagetran import mailbox
from .perinfo import personal_information
from . import homepage
