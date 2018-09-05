from . import generate
import json
import random
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

from datetime import datetime
current_time = datetime.utcnow()

engine = create_engine(
    'mysql+pymysql://arlen:5609651Wmm!@47.94.138.25:3306/papergenerate?charset=utf8', encoding="utf-8", echo=True,
    pool_recycle=21600, pool_size=8, max_overflow=5)
DBSession = sessionmaker(bind=engine)


@generate.route('/byhand', methods=['GET', 'POST'])
@login_required
def generatepage():
    if request.method=='POST':
        pass
    else:
        user = current_user._get_current_object()
        if user.course == 0:
            privilege = '管理员'
        else:
            privilege = '普通用户'
        return render_template('byhand.html', user=user, privilege=privilege,current_time=current_time)


@generate.route('/auto', methods=['GET', 'POST'])
@login_required
def managepaperpage():
    if request.method=='POST':
        danx=int(request.form['danxuan'])
        duox=int(request.form['duoxuan'])
        pand=int(request.form['panduan'])
        jiand=int(request.form['jianda'])
        tiank=int(request.form['tiankong'])
        dat=int(request.form['dati'])
        session=DBSession()
        pansession=DBSession()
        jiansession=DBSession()
        tiansession=DBSession()
        datisession=DBSession()
        xuanzeti=session.query(question).filter(question.type==4).all()
        xuanzetilen=xuanzeti.count()
        panduanti=pansession.query(question).filter(question.type==6).all()
        panduantilen=panduanti.count()
        jiandati=jiansession.query(question).filter(question.type==1).all()
        jiandatilen=jiandati.count()
        tiankongti=tiansession.query(question).filter(question.type==2).all()
        tiankongtilen=tiankongti.count()
        dati=datisession.query(question).filter(question.type==3).all()
        datilen=dati.count()
        for i in range(0,danx):
            nowdanxuan=xuanzeti[random.randint(0,xuanzetilen)]
            paper.danxuan.append(nowdanxuan.qid)



    else:
        user = current_user._get_current_object()
        if user.course == 0:
            privilege = '管理员'
        else:
            privilege = '普通用户'
        return render_template('auto.html', user=user, privilege=privilege,current_time=current_time)


