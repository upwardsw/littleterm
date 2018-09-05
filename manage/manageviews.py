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

from datetime import datetime
current_time = datetime.utcnow()

engine = create_engine(
    'mysql+pymysql://arlen:5609651Wmm!@47.94.138.25:3306/papergenerate?charset=utf8', encoding="utf-8", echo=True,
    pool_recycle=21600, pool_size=8, max_overflow=5)
DBSession = sessionmaker(bind=engine)


@manage.route('/unchoice',methods=['GET','POST'])
def manageunchoice():
    if request.method=='POST':
        session=DBSession()
        qtype=request.form['qtype']
        try:start=int(request.form['start'])
        except:start=0
        data=session.query(question).filter(question.type==qtype).limit(10).offset(start)
        result=[]
        newsession=DBSession()
        for i in data:
            questionanswer=newsession.query(qanswer).filter(qanswer.question_qid==i.qid).first()
            #result.append([i.qid,i.question,i.type,i.level,i.course,questionanswer.qanswer])
            result.append(dict(qid=i.qid,question=i.question,type=i.type,level=i.level,course=i.course,delornot=i.delornot,answer=questionanswer.qanswer))
        print(result)
        # return Response(response=json.dumps(result))
        user = current_user._get_current_object()
        privilege = '普通用户'
        if user.course == 0: privilege = '管理员'
        return render_template('manageunchoice.html',result=result,privilege=privilege,current_time=current_time,start=start,username=user.username)
    else:
        session = DBSession()
        newsession = DBSession()
        start = 0
        data = session.query(question).filter(question.type == 3).limit(10).offset(start)
        result = []
        newsession = DBSession()
        for i in data:
            questionanswer = newsession.query(qanswer).filter(qanswer.question_qid == i.qid).first()
            # result.append([i.qid,i.question,i.type,i.level,i.course,questionanswer.qanswer])
            result.append(
                dict(qid=i.qid, question=i.question, type=i.type, level=i.level, course=i.course, delornot=i.delornot,
                     answer=questionanswer.qanswer))
        user = current_user._get_current_object()
        privilege = '普通用户'
        if user.course == 0: privilege = '管理员'
        return render_template('manageunchoice.html', result=result, privilege=privilege, current_time=current_time, start=start, username=user.username)


@manage.route('/choice',methods=['GET','POST'])
@login_required
def managechoice():
    if request.method=='POST':
        session = DBSession()
        try:
            start = int(request.form['start'])
        except:
            start = 0
        print(start)
        data = session.query(question).filter(question.type ==4).limit(10).offset(start)
        # for n in data:print(n.qid)
        print()
        result = []
        newsession = DBSession()
        for i in data:
            questionanswer = newsession.query(choices).filter(choices.question_qid == i.qid).all()
            tureanswer=''
            wronganswer=''
            for j in questionanswer:
                if j.torf==1:
                    tureanswer=tureanswer+' {0}'.format(j.choice)
                    #tureanswer.append(dict(cid=j.cid,choice=j.choice))
                if j.torf==0:
                    wronganswer=wronganswer+' {0}'.format(j.choice)
                    #wronganswer.append(dict(cid=j.cid,choice=j.choice))
            result.append(dict(qid=i.qid,question=i.question,type=i.type,level=i.level,course=i.course,right=tureanswer,wrong=wronganswer,delornot=i.delornot))
        print(result)
        user = current_user._get_current_object()
        privilege = '普通用户'
        if user.course == 0: privilege = '管理员'
        return render_template('managechoice.html',result=result,current_time=current_time,start=start,username=user.username, privilege=privilege)
    else:
        session = DBSession()
        try:
            start = int(request.form['start'])
        except:
            start = 0
        data = session.query(question).filter(question.type == 4).limit(10).offset(start)
        # for n in data:print(n.qid)
        result = []
        newsession = DBSession()
        for i in data:
            questionanswer = newsession.query(choices).filter(choices.question_qid == i.qid).all()
            tureanswer = []
            wronganswer = []
            for j in questionanswer:
                if j.torf == 1:
                    tureanswer.append(j.choice)
                if j.torf == 0:
                    # wronganswer = wronganswer + ' {0}'.format(str(j.choice))
                    wronganswer.append(j.choice)
            result.append(
                dict(qid=i.qid, question=i.question, type=i.type, level=i.level, course=i.course, right=tureanswer,
                     wrong=wronganswer))
        print(result)
        user = current_user._get_current_object()
        privilege = '普通用户'
        if user.course == 0: privilege = '管理员'
        return render_template('managechoice.html', result=result, current_time=current_time, start=start, username=user.username, privilege=privilege)


@manage.route('/changeunchoice/',methods=['GET','POST'])
@login_required
def changequestion(qid):
    if request.method=='POST':
        session=DBSession()
        newsession=DBSession()
        qid=request.form['qid']
        questiontext=request.form['question']
        dornot=request.form['delornot']
        level=request.form['level']
        course=request.form['course']
        newanswer=request.form['qanswer']
        print(qid,questiontext,dornot,level,course,newanswer)
        cquestion=session.query(question).filter(question.qid==qid).first()
        cqanswer=newsession.query(qanswer).filter(qanswer.question_qid==cquestion.qid).first()
        cquestion.question=questiontext
        cquestion.delornot=dornot
        cquestion.level=level
        cquestion.course=course
        cqanswer.qanswer=newanswer
        session.commit()
        newsession.commit()

        session.close()
        newsession.close()
        return render_template('changeunchoice.html',question=cquestion,cqanswer=cqanswer)
    else:
        session=DBSession()
        newsession=DBSession()
        nowqs=session.query(question).filter(question.qid==qid).first()
        nowanswer=newsession.query(qanswer).filter(qanswer.question_qid==qid).first()
        return render_template('changeunchoice.html',answer=nowanswer,question=nowqs)


@manage.route('/changes',methods=['POST','GET'])
@login_required
def changes():
    if request.method=='POST':
        session=DBSession()
        newsession=DBSession()
        qid=request.form['qid']
        questiontext=request.form['question']
        dornot=request.form['delornot']
        level=request.form['level']
        course=request.form['course']
        newanswer=request.form['qanswer']
        print(qid,questiontext,dornot,level,course,newanswer)
        cquestion=session.query(question).filter(question.qid==qid).first()
        cqanswer=newsession.query(qanswer).filter(qanswer.question_qid==cquestion.qid).first()
        cquestion.question=questiontext
        cquestion.delornot=dornot
        cquestion.level=level
        cquestion.course=course
        cqanswer.qanswer=newanswer
        session.commit()
        newsession.commit()

        session.close()
        newsession.close()
        return render_template('changeunchoice.html',question=cquestion,cqanswer=cqanswer)
    else:return render_template('test.html')

@manage.route('/changechoice',methods=['GET','POST'])
def changechoice():
    if request.method=='POST':
        session=DBSession()
        newsession=DBSession()
        qid=request.form['qid']
        questiontext=request.form['question']
        dornot=request.form['delornot']
        level=request.form['level']
        course=request.form['course']
        newanswer=request.form['answer']
        wronganswer=request.form['wronganswer']
        print(qid,questiontext,dornot,level,course,newanswer,wronganswer)

        cquestion=session.query(question).filter(question.qid==qid).first()
        deldata=newsession.query(choices).filter(choices.question_qid==cquestion.qid).all()
        for m in deldata:
            newsession.delete(m)
        # cqanswer=newsession.query(qanswer).filter(qanswer.question_qid==cquestion.qid).first()
        cquestion.question=questiontext
        cquestion.delornot=dornot
        cquestion.level=level
        cquestion.course=course

        p1 = re.compile(r"[[](.*?)[]]", re.S)  # 最小匹配
        answer = re.findall(p1, newanswer)
        wronganswer = re.findall(p1, wronganswer)
        for i in answer:
            addchoice = choices(question_qid=cquestion.qid, choice=i, torf=True)
            newsession.add(addchoice)
            newsession.commit()
        for j in wronganswer:
            addwronganswer = choices(question_qid=cquestion.qid, choice=j, torf=False)
            newsession.add(addwronganswer)
            newsession.commit()

        # cqanswer.qanswer=newanswer
        session.commit()

        session.close()
        newsession.close()
    else:return render_template('changechoice.html')












