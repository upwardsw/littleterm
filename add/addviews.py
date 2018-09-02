from . import add
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


@add.route('/dati',methods=['GET','POST'])
@login_required
def adddati():
    if request.method == 'POST':
        session = DBSession()
        answer = request.form['answer']
        addquestion = request.form['question']
        level = request.form['level']
        course=request.form['course']

        data=question()
        data.question=addquestion
        data.level=level
        data.delornot=False
        data.type=3
        data.course=course
        session.add(data)
        session.commit()

        print(data.qid)


        addanswer=qanswer()
        addanswer.question_qid=data.qid
        addanswer.qanswer=answer
        session.add(addanswer)
        session.commit()

        session.close()
        return render_template('adddati.html',msg='提交成功!')
    else:
        return render_template('adddati.html')


@add.route('/tiankongti',methods=['GET','POST'])
@login_required
def addtiankong():
    if request.method == 'POST':
        session = DBSession()
        answer = request.form['answer']
        addquestion = request.form['question']
        level = request.form['level']
        course = request.form['course']

        data = question()
        data.question = addquestion
        data.level = level
        data.delornot = False
        data.type = 2
        data.course = course
        session.add(data)
        session.commit()

        addanswer = qanswer()
        addanswer.question_qid = data.qid
        addanswer.qanswer = answer
        session.add(addanswer)
        session.commit()

        session.close()
        return render_template('addtiankong.html', msg='提交成功!')
    else:
        return render_template('addtiankong.html')


@add.route('/choice',methods=['GET','POST'])
@login_required
def addchoice():
    if request.method == 'POST':
        session = DBSession()
        answer = request.form['answer']
        wronganswer=request.form['wronganswer']
        addquestion = request.form['question']
        level = request.form['level']
        course = request.form['course']
        p1 = re.compile(r"[[](.*?)[]]", re.S)  # 最小匹配
        answer=re.findall(p1, answer)
        wronganswer=re.findall(p1, wronganswer)

        data = question()
        data.question = addquestion
        data.level = level
        data.delornot = False
        if len(answer)==1:data.type=5
        else:data.type=4
        data.course = course
        session.add(data)
        session.commit()

        for i in answer:
            addchoice=choices(question_qid=data.qid,choice=i,torf=True)
            session.add(addchoice)
            session.commit()
        for j in wronganswer:
            addwronganswer=choices(question_qid=data.qid,choice=j,torf=False)
            session.add(addwronganswer)
            session.commit()

        session.close()
        return render_template('addchoice.html',msg='提交成功!')



    else:
        return render_template('addchoice.html')


@add.route('/judgeti',methods=['GET','POST'])
@login_required
def addjudge():
    if request.method == 'POST':
        session = DBSession()
        answer = request.form['answer']
        addquestion = request.form['question']
        level = request.form['level']
        course = request.form['course']


        data = question()
        data.question = addquestion
        data.level = level
        data.delornot = False
        data.type = 6
        data.course = course
        session.add(data)
        session.commit()

        addanswer=qanswer(question_qid=data.qid,qanswer=answer)
        session.add(addanswer)
        session.commit()
        session.close()
        return render_template('addjudege.html',msg='提交成功!')
    else:
        return render_template('addjudege.html')


@add.route('/jiandati',methods=['GET','POST'])
@login_required
def addjiandati():
    if request.method == 'POST':
        session = DBSession()
        answer = request.form['answer']
        addquestion = request.form['question']
        level = request.form['level']
        course=request.form['course']

        data=question()
        data.question=addquestion
        data.level=level
        data.delornot=False
        data.type=1
        data.course=course
        session.add(data)
        session.commit()

        print(data.qid)

        addanswer=qanswer()
        addanswer.question_qid=data.qid
        addanswer.qanswer=answer
        session.add(addanswer)
        session.commit()

        session.close()
        return render_template('addjiandati.html',msg='提交成功!')
    else:
        return render_template('addjiandati.html')