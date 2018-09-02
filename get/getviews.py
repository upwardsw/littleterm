from . import get
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


@get.route('/username')
@login_required
def getusername():
    cuser = current_user._get_current_object()
    data = '{}'.format(cuser.username)
    return Response(response=data)


@get.route('/userid')
@login_required
def getuserid():
    cuser = current_user._get_current_object()
    data = '{}'.format(cuser.userid)
    return Response(response=data)


@get.route('/useremail')
@login_required
def getuseremail():
    cuser = current_user._get_current_object()
    data = '{}'.format(cuser.email)
    return Response(response=data)


@get.route('/userprivilege')
@login_required
def getuserprivilege():
    cuser = current_user._get_current_object()
    privilege = '普通用户'
    if cuser.course == 0: privilege = '管理员'
    return Response(response=privilege)


@get.route('/answer/<qid>')
@login_required
def getanswer(qid):
    session = DBSession()
    try:
        data = session.query(question).filter(question.qid == qid).first()
        print(data)
        if data.delornot == 1:
            return '该问题已失效!'
        else:
            # jiandati
            if data.type == 1:
                answer = '{}'.format(session.query(qanswer).filter(qanswer.question_qid == data.qid).first().qanswer)
                # print(session.query(qanswer).filter(qanswer.question_qid == data.qid).first().qanswer)
                return Response(response=json.dumps(answer, ensure_ascii=False))
            # tiankong
            if data.type == 2:
                answer = '{}'.format(session.query(qanswer).filter(qanswer.question_qid == data.qid).first().qanswer)
                return Response(response=json.dumps(answer, ensure_ascii=False))
            # dati
            if data.type == 3:
                answer = '{}'.format(session.query(qanswer).filter(qanswer.question_qid == data.qid).first().qanswer)
                return Response(response=json.dumps(answer, ensure_ascii=False))
            #  multi choice
            if data.type == 4:
                answer = []
                cs = session.query(choices).filter(choices.question_qid == data.qid).all()
                for c in cs:
                    if c.torf == 1:
                        answer.append(c.choice)
                return Response(response=json.dumps(answer, ensure_ascii=False))
            # simple choice
            if data.type == 5:
                cs = session.query(choices).filter(choices.question_qid == data.qid).all()
                for c in cs:
                    if c.torf == 1:
                        answer = c.choice
                        return Response(response=json.dumps(answer, ensure_ascii=False))
            # judge
            if data.type == 6:
                answer = '{}'.format(session.query(qanswer).filter(qanswer.question_qid == data.qid).first().qanswer)
                return Response(response=json.dumps(answer, ensure_ascii=False))
    except:
        return Response(response=json.dumps('该问题不存在!', ensure_ascii=False),status=500)
    session.close()


@get.route('/question/<qid>')
@login_required
def getquestion(qid):
    session = DBSession()
    data = session.query(question).filter(question.qid == qid).first()
    data = dict(q=data.question, qid=qid, type=data.type, delornot=data.delornot, level=data.level, course=data.course)
    print(data)
    session.close()
    return Response(response=json.dumps(data, ensure_ascii=False))