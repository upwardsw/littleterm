from . import manage
import json
import re

from flask import Flask, url_for, Response
from flask.json import jsonify
from flask_login import LoginManager
from flask import redirect, request, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import *
from sqlalchemy.orm import *

from tables import User, question, qanswer, choices


engine = create_engine(
    'mysql+pymysql://arlen:5609651Wmm!@47.94.138.25:3306/papergenerate?charset=utf8', encoding="utf-8", echo=True,
    pool_recycle=21600, pool_size=8, max_overflow=5)
DBSession = sessionmaker(bind=engine)


@manage.route('/main',methods=['GET','POST'])
def managemain():
    user = current_user._get_current_object()
    privilege = 'user'
    if user.course == 0: privilege = 'admin'
    return render_template('manage.html',username=user.username,privilege=privilege)