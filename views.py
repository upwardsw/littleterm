import json
import os
import random
import re

from add import add as add_blueprint
from get import get as get_blueprint
from manage import manage as manage_blueprint
from generate import generate as generate_blueprint

from flask import Flask, url_for, Response, send_from_directory, make_response
from flask.json import jsonify
from flask_login import LoginManager
from flask import redirect, request, render_template
from flask_bootstrap import Bootstrap
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import *
from sqlalchemy.orm import *
from flask_moment import Moment
from flask_cors import CORS

from datetime import datetime
from tables import User, question, qanswer, choices, paper

app = Flask(__name__)
app.config['SECRET_KEY'] = '`~1!2@3#4$5%6^7&8*9(0)-_=+'
login_manager = LoginManager()
login_manager.init_app(app)  # flask-login模块初始化
Bootstrap(app)  # BootStrap支持
login_manager.login_view = "login"
login_manager.session_protection = "strong"
moment = Moment(app)  # 本地化时间支持
CORS(app)  # 跨域请求支持

current_time = datetime.utcnow()
engine = create_engine(
    'mysql+pymysql://arlen:5609651Wmm!@47.94.138.25:3306/papergenerate?charset=utf8', encoding="utf-8", echo=True,
    pool_recycle=21600, pool_size=8, max_overflow=5)
DBSession = sessionmaker(bind=engine)

nowpaper = paper()

# 添加模块
app.register_blueprint(add_blueprint, )
# 获取模块
app.register_blueprint(get_blueprint)
# 管理模块
app.register_blueprint(manage_blueprint)
# 生成模块
app.register_blueprint(generate_blueprint)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        session = DBSession()
        email = request.form['useremail']
        username = request.form['username']
        password = request.form['userpassword']
        course = request.form['course']
        password = generate_password_hash(password)
        print(email)
        if session.query(User).filter(User.email == email).first():
            return render_template('register.html', msg='该邮箱已被注册！', current_time=current_time)
        else:
            adduser = User(password=password, username=username, email=email, course=course)
            session.add(adduser)
            session.commit()
            os.makedirs(os.getcwd() + '/static/files/{0}'.format(adduser.userid))
            session.close()

            return redirect(url_for('login'))
    else:
        return render_template('register.html', current_time=current_time)


@login_manager.user_loader
def load_user(user_id):
    session = DBSession()
    user = session.query(User).filter(User.userid == user_id).first()
    session.close()
    return user


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        next = request.form['nexturl']
        print(next)
        if next == 'None': next = url_for('main')
        email = request.form['email']
        password = request.form['password']
        try:
            a0 = request.form['remember']
            rem = True
        except:
            rem = False
        connect = DBSession()
        try:
            user = connect.query(User).filter(User.email == email).first()
            print(user.get_id())
            if email != '' and check_password_hash(user.password, password):
                login_user(user, remember=rem)
                connect.close()
                return redirect(next or url_for('main'))
                # return render_template('main.html', user=user.username,current_time=current_time)
            else:
                connect.close()
                return render_template('login.html', msg='登录失败，请检查邮箱和密码！', current_time=current_time)
        except:
            connect.close()
            return render_template('login.html', msg='用户名'.format(email), current_time=current_time)
    else:
        next = request.values.get('next')
        print(next)
        return render_template('login.html', nexturl=next, current_time=current_time)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    # load current user to class user
    user = current_user._get_current_object()
    if user.course == 0:
        privilege = '管理员'
    else:
        privilege = '普通用户'
    return render_template('main.html', user=user, privilege=privilege, current_time=current_time)


@app.route('/addunchoice', methods=['GET', 'POST'])
@login_required
def addunchoice():
    if request.method == 'POST':
        qid = str(request.get_data('questionid'), encoding="utf-8")
        for i in qid:
            if i == '=':
                temp = qid[qid.index(i) + 1:]
        qid = int(temp)
        print(qid)
        session = DBSession()
        data = session.query(question).filter(question.qid == qid).first()
        nowpaper.addquestion(data)
        return Response(status=200)


@app.route('/adddanchoice', methods=['GET', 'POST'])
@login_required
def adddanchoice():
    if request.method == 'POST':
        qid = str(request.get_data('questionid'), encoding="utf-8")
        for i in qid:
            if i == '=':
                temp = qid[qid.index(i) + 1:]
        qid = int(temp)
        print(qid)
        session = DBSession()
        data = session.query(question).filter(question.qid == qid).first()
        nowpaper.adddanxuan(data)
        return Response(status=200)


@app.route('/addduochoice', methods=['GET', 'POST'])
@login_required
def addduochoice():
    if request.method == 'POST':
        qid = str(request.get_data('questionid'), encoding="utf-8")
        for i in qid:
            if i == '=':
                temp = qid[qid.index(i) + 1:]
        qid = int(temp)
        print(qid)
        session = DBSession()
        data = session.query(question).filter(question.qid == qid).first()
        nowpaper.addduoxuan(data)
        return Response(status=200)


@app.route('/shijuan',methods=['GET','POST'])
@login_required
def shijaun():
    if request.method=='POST':
        danx=int(request.form['danxuan'])
        duox=int(request.form['duoxuan'])
        pand=int(request.form['panduan'])
        jiand=int(request.form['jianda'])
        tiank=int(request.form['tiankong'])
        dat=int(request.form['dati'])
        newsession=DBSession()
        pansession=DBSession()
        jiansession=DBSession()
        tiansession=DBSession()
        datisession=DBSession()
        xuanzeti=newsession.query(question).filter(question.type==4).all()
        xuanzetilen=newsession.query(question).filter(question.type==4).count()
        panduanti=pansession.query(question).filter(question.type==6).all()
        panduantilen=pansession.query(question).filter(question.type==6).count()
        jiandati=jiansession.query(question).filter(question.type==1).all()
        jiandatilen=jiansession.query(question).filter(question.type==1).count()
        tiankongti=tiansession.query(question).filter(question.type==2).all()
        tiankongtilen=tiansession.query(question).filter(question.type==2).count()
        dati=datisession.query(question).filter(question.type==3).all()
        datilen=datisession.query(question).filter(question.type==3).count()
        for i in range(0,danx):
            nowdanxuan=xuanzeti[random.randint(0,xuanzetilen-1)]
            paper.danxuan.append(nowdanxuan.qid)
        for j in range(0,duox):
            nowduoxuan=xuanzeti[random.randint(0,xuanzetilen-1)]
            paper.duoxuan.append(nowduoxuan.qid)
        for n in range(0,pand):
            nowpanduan=panduanti[random.randint(0,panduantilen-1)]
            paper.pandaun.append(nowpanduan.qid)
        for k in range(0,jiand):
            nowjianda=jiandati[random.randint(0,jiandatilen-1)]
            paper.jianda.append(nowjianda.qid)
        for m in range(0,tiank):
            nowtiankong=tiankongti[random.randint(0,tiankongtilen-1)]
            paper.tiankong.append(nowtiankong.qid)
        for x in range(0,dat):
            nowdati=dati[random.randint(0,datilen-1)]
            paper.dati.append(nowdati.qid)
        user = current_user._get_current_object()
        if user.course == 0:
            privilege = '管理员'
        else:
            privilege = '普通用户'
        result = []
        session = DBSession()
        for i in paper.danxuan:
            data = session.query(question).filter(question.qid == i).first()
            result.append([data.qid, data.question, '单选', data.level, data.course])
        for j in paper.duoxuan:
            data = session.query(question).filter(question.qid == j).first()
            result.append([data.qid, data.question, '多选', data.level, data.course])
        for k in paper.jianda:
            data = session.query(question).filter(question.qid == k).first()
            result.append([data.qid, data.question, '简答', data.level, data.course])
        for n in paper.pandaun:
            data = session.query(question).filter(question.qid == n).first()
            result.append([data.qid, data.question, '判断', data.level, data.course])
        for m in paper.tiankong:
            data = session.query(question).filter(question.qid == m).first()
            result.append([data.qid, data.question, '填空', data.level, data.course])
        for x in paper.dati:
            data = session.query(question).filter(question.qid == x).first()
            result.append([data.qid, data.question, '大题', data.level, data.course])
        return render_template('showshijuan.html', user=user, privilege=privilege, current_time=current_time,
                               result=result)
    else:
        user = current_user._get_current_object()
        if user.course == 0:
            privilege = '管理员'
        else:
            privilege = '普通用户'
        result = []
        session = DBSession()
        # 遍历试卷所有题目，获取题目信息并返回
        for i in paper.danxuan:
            data = session.query(question).filter(question.qid == i).first()
            result.append([data.qid, data.question, '单选', data.level, data.course])
        for j in paper.duoxuan:
            data = session.query(question).filter(question.qid == j).first()
            result.append([data.qid, data.question, '多选', data.level, data.course])
        for k in paper.jianda:
            data = session.query(question).filter(question.qid == k).first()
            result.append([data.qid, data.question, '简答', data.level, data.course])
        for n in paper.pandaun:
            data = session.query(question).filter(question.qid == n).first()
            result.append([data.qid, data.question, '判断', data.level, data.course])
        for m in paper.tiankong:
            data = session.query(question).filter(question.qid == m).first()
            result.append([data.qid, data.question, '填空', data.level, data.course])
        for x in paper.dati:
            data = session.query(question).filter(question.qid == x).first()
            result.append([data.qid, data.question, '大题', data.level, data.course])
        return render_template('showshijuan.html', user=user, privilege=privilege, current_time=current_time, result=result)


@app.route('/delall',methods=['POST'])
@login_required
def delall():
    paper.clear(paper)
    return Response(status=200)


@app.route('/deletequestion', methods=['POST'])
@login_required
def deletequestion():
    if request.method == 'POST':
        qid = str(request.get_data('qid'), encoding="utf-8")
        for i in qid:
            if i == '=':
                temp = qid[qid.index(i) + 1:]
        qid = int(temp)
        print(qid)
        session = DBSession()
        data = session.query(question).filter(question.qid == qid).first()
        if data.type == 1: del paper.jianda[paper.jianda.index(qid)]
        if data.type == 2: del paper.tiankong[paper.tiankong.index(qid)]
        if data.type == 3: del paper.dati[paper.dati.index(qid)]
        if data.type == 6: del paper.pandaun[paper.pandaun.index(qid)]
        if data.type == 4:
            if qid in paper.danxuan:del paper.danxuan[paper.danxuan.index(qid)]
            else:del paper.duoxuan[paper.duoxuan.index(qid)]
        return Response(status=200)


@app.route('/paper/<filename>',methods=['POST','GET'])
@login_required
def downpaper(filename):
    user = current_user._get_current_object()
    response = make_response(
        send_from_directory('static/files/{0}/{1}'.format(user.userid, filename), 'question.txt', as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

@app.route('/answer/<filename>',methods=['POST','GET'])
@login_required
def downanswer(filename):
    user=current_user._get_current_object()
    response = make_response(send_from_directory('static/files/{0}/{1}'.format(user.userid,filename), 'answer.txt', as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response



def generateRand(min,max,num,result):
    counter=1
    running=True
    while running:
        tempInt=random.randint(min,max-1); # 生成一个范围内的临时随机数，
        if(counter<=num): # 先看随机数的总个数是不是够了，如果不够
            if(tempInt not in result): # 再检查当前已经生成的临时随机数是不是已经存在，如果不存在
                result.append(tempInt); #则将其追加到结果List中
                counter+=1;# 然后将表示有效结果的个数加1. 请注意这里，如果临时随机数已经存在，则此if不成立，那么将直接执行16行，counter不用再加1
        else:
            break
    return result


@app.route('/file',methods=['POST','GET'])
@login_required
def savefile():
    if request.method=='POST':
        ABCD=['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
        session=DBSession()
        truesession=DBSession()
        wrongsession=DBSession()
        filename=request.form['papername']
        user=current_user._get_current_object()
        os.makedirs(os.getcwd() + '/static/files/{0}/{1}'.format(user.userid,filename))
        txtanswer=[]
        with open(os.getcwd() + '/static/files/{0}/{1}/question.txt'.format(user.userid, filename), 'a',encoding='utf-8') as f:
            # 最后将问题写入文件并清空所有数组
            f.writelines('试卷 {0}\n'.format(filename))
            if len(paper.danxuan) != 0:
                # 写入标题单选题
                title = '{0}.{1}'.format(paper.gettitlenum(paper), '单选题')
                f.write('{0}\n'.format(title))
                paper.title += 1
                for i in paper.danxuan:
                    resultlist=[]
                    data=session.query(question).filter(question.qid==i).first()
                    f.writelines('{0}.{1}\n'.format(paper.xuhao+1,data.question))
                    answer=truesession.query(choices).filter(choices.question_qid==i and choices.torf==1).all()
                    answercount=truesession.query(choices).filter(choices.question_qid==i and choices.torf==1).count()
                    wronganswer=wrongsession.query(choices).filter(choices.question_qid==i and choices.torf==0).all()
                    wronganswercount=wrongsession.query(choices).filter(choices.question_qid==i and choices.torf==0).count()
                    fourchoices=[] # 4个选项
                    newanswer=answer[random.randint(0,answercount-1)]  # 随机从正确选项中选出一个
                    fourchoices.append(newanswer.choice) # 存入选项数组
                    txtanswer.append([paper.xuhao+1,newanswer.choice]) # 存入答案数组
                    paper.xuhao+=1
                    resultlist=generateRand(0,wronganswercount,3,resultlist) # 随机从错误选项中抽取3个选项
                    # 将抽出的3个错误选项存入选项数组
                    for j in resultlist:
                        fourchoices.append(wronganswer[j].choice)
                    random.shuffle(fourchoices) # 打乱选项数组
                    # 将4个选项写入文件
                    for k in range(0,4):
                        f.writelines('{0}.{1}\n'.format(ABCD[k],fourchoices[k]))
                    f.writelines('\n')
            if len(paper.duoxuan) != 0:
                # 写入标题多选题
                title = '{0}.{1}'.format(paper.gettitlenum(paper), '多选题')
                f.write('{0}\n'.format(title))
                paper.title += 1
                for i in paper.duoxuan:
                    resultlist = [] # 随机数数组
                    fourchoices = [] # 选项数组
                    mulchoice=[] # 正确选项数组
                    data = session.query(question).filter(question.qid == i).first()
                    f.writelines('{0}.{1}\n'.format(paper.xuhao + 1, data.question))
                    # 获取数据库中正确选项和正确选项数量
                    answer = truesession.query(choices).filter(choices.question_qid == i and choices.torf == 1).all()
                    answercount = truesession.query(choices).filter(choices.question_qid == i and choices.torf==1).count()
                    # 获取数据库中错误选项和错误选项数量
                    wronganswer = wrongsession.query(choices).filter(
                        choices.question_qid == i and choices.torf == 0).all()
                    wronganswercount = wrongsession.query(choices).filter(
                        choices.question_qid == i and choices.torf == 0).count()
                    # 生成需要的正确选项数量和错误选项数量
                    answernum=random.randint(0,answercount-1)
                    wronganswernum=random.randint(0,wronganswercount-1)
                    # 生成正确选项数量个数的正确选项下标
                    resultlist=generateRand(0, answercount, answernum,resultlist)
                    # 根据下标将需要的正确选项写入选项数组
                    for j in resultlist:
                        nowanswer=answer[j]
                        fourchoices.append(nowanswer.choice)
                        mulchoice.append(nowanswer.choice)
                    resultlist = []
                    # 生成错误选项数量个数的错误选项下标
                    resultlist=generateRand(0, wronganswercount, wronganswernum,  resultlist)
                    # 根据下标将需要的错误选项写入选项数组
                    for k in resultlist:
                        nowanswer = wronganswer[k]
                        fourchoices.append(nowanswer.choice)
                    random.shuffle(fourchoices) # 打乱选项数组
                    # 将选项数组写入文件
                    for m in range(0,len(fourchoices)):
                        f.writelines('{0}.{1}\n'.format(ABCD[m],fourchoices[m]))
                    txtanswer.append([paper.xuhao+1,"".join(mulchoice)]) # 将正确选项写入答案
                    f.writelines('\n')
                    paper.xuhao+=1


            if len(paper.tiankong) != 0:
                # 写入标题填空题
                title = '{0}.{1}'.format(paper.gettitlenum(paper), '填空题')
                f.write('{0}\n'.format(title))
                paper.title += 1
                # 遍历添加到试卷的所有填空题qid
                for i in paper.tiankong:
                    data=session.query(question).filter(question.qid==i).first()
                    answer=truesession.query(qanswer).filter(qanswer.question_qid==i).first()
                    f.writelines('{0}.{1}\n'.format(paper.xuhao+1,data.question))
                    txtanswer.append([paper.xuhao+1,answer.qanswer])
                    paper.xuhao+=1
                    f.writelines('\n')
            if len(paper.pandaun) != 0:
                # 写入标题判断题
                title = '{0}.{1}'.format(paper.gettitlenum(paper), '判断题')
                f.write('{0}\n'.format(title))
                paper.title += 1
                # 遍历添加到试卷的所有判断题qid
                for i in paper.pandaun:
                    data=session.query(question).filter(question.qid==i).first()
                    answer=truesession.query(qanswer).filter(qanswer.question_qid==i).first()
                    f.writelines('{0}.{1}\n'.format(paper.xuhao+1,data.question))
                    txtanswer.append([paper.xuhao+1,answer.qanswer])
                    paper.xuhao+=1
                    f.writelines('\n')
            if len(paper.jianda) != 0:
                # 写入标题简答题
                title = '{0}.{1}'.format(paper.gettitlenum(paper), '简答题')
                f.write('{0}\n'.format(title))
                paper.title += 1
                # 遍历添加到试卷的所有简答题qid
                for i in paper.jianda:
                    data=session.query(question).filter(question.qid==i).first()
                    answer=truesession.query(qanswer).filter(qanswer.question_qid==i).first()
                    f.writelines('{0}.{1}\n'.format(paper.xuhao+1,data.question))
                    txtanswer.append([paper.xuhao+1,answer.qanswer])
                    paper.xuhao+=1
                    f.writelines('\n')
            if len(paper.dati) != 0:
                # 写入标题大题
                title = '{0}.{1}'.format(paper.gettitlenum(paper), '大题')
                f.write('{0}\n'.format(title))
                paper.title += 1
                # 遍历添加到试卷的所有大题qid
                for i in paper.dati:
                    data=session.query(question).filter(question.qid==i).first()
                    answer=truesession.query(qanswer).filter(qanswer.question_qid==i).first()
                    f.writelines('{0}.{1}\n'.format(paper.xuhao+1,data.question))
                    txtanswer.append([paper.xuhao+1,answer.qanswer])
                    paper.xuhao+=1
                    f.writelines('\n')
        with open(os.getcwd() + '/static/files/{0}/{1}/answer.txt'.format(user.userid, filename), 'a',encoding='utf-8') as aw:
            aw.writelines('答案\n')
            for i in txtanswer:
                aw.writelines('{0}.{1}\n'.format(i[0],i[1]))
        paper.clear(paper)
        txtanswer=[]
        return redirect(url_for('savefile'))
    else:
        user=current_user._get_current_object()
        filelist=os.listdir(os.getcwd()+'/static/files/{0}'.format(user.userid))
        print(filelist)
        user = current_user._get_current_object()
        if user.course == 0:
            privilege = '管理员'
        else:
            privilege = '普通用户'
        return render_template('download.html', user=user, privilege=privilege, current_time=current_time,result=filelist)



# @app.route('/generatepage', methods=['GET', 'POST'])
# @login_required
# def generatepage():
#     return '!!!!'
#
#
# @app.route('/managepaperpage', methods=['GET', 'POST'])
# @login_required
# def managepaperpage():
#     return '!!!!'
#
#
# @app.route('/managequestionpage', methods=['GET', 'POST'])
# @login_required
# def managequestionpage():
#     return '!!!!'
#
#
# @app.route('/autogeneratepage', methods=['GET', 'POST'])
# @login_required
# def autogeneratepage():
#     return '!!!!'
#
#
# @app.route('/getusername')
# @login_required
# def getusername():
#     cuser = current_user._get_current_object()
#     data = '{}'.format(cuser.username)
#     return Response(response=data)
#
#
# @app.route('/getuserid')
# @login_required
# def getuserid():
#     cuser = current_user._get_current_object()
#     data = '{}'.format(cuser.userid)
#     return Response(response=data)
#
#
# @app.route('/getuseremail')
# @login_required
# def getuseremail():
#     cuser = current_user._get_current_object()
#     data = '{}'.format(cuser.email)
#     return Response(response=data)
#
#
# @app.route('/getuserprivilege')
# @login_required
# def getuserprivilege():
#     cuser = current_user._get_current_object()
#     privilege = 'user'
#     if cuser.course == 0: privilege = 'admin'
#     return Response(response=privilege)
#
#
# @app.route('/getanswer/<qid>')
# @login_required
# def getanswer(qid):
#     session = DBSession()
#     try:
#         data = session.query(question).filter(question.qid == qid).first()
#         print(data)
#         if data.delornot == 1:
#             return 'question id is invalid!'
#         else:
#             # jiandati
#             if data.type == 1:
#                 answer = '{}'.format(session.query(qanswer).filter(qanswer.question_qid == data.qid).first().qanswer)
#                 # print(session.query(qanswer).filter(qanswer.question_qid == data.qid).first().qanswer)
#                 return Response(response=json.dumps(answer, ensure_ascii=False))
#             # tiankong
#             if data.type == 2:
#                 answer = '{}'.format(session.query(qanswer).filter(qanswer.question_qid == data.qid).first().qanswer)
#                 return Response(response=json.dumps(answer, ensure_ascii=False))
#             # dati
#             if data.type == 3:
#                 answer = '{}'.format(session.query(qanswer).filter(qanswer.question_qid == data.qid).first().qanswer)
#                 return Response(response=json.dumps(answer, ensure_ascii=False))
#             #  multi choice
#             if data.type == 4:
#                 answer = []
#                 cs = session.query(choices).filter(choices.question_qid == data.qid).all()
#                 for c in cs:
#                     if c.torf == 1:
#                         answer.append(c.choice)
#                 return Response(response=json.dumps(answer, ensure_ascii=False))
#             # simple choice
#             if data.type == 5:
#                 cs = session.query(choices).filter(choices.question_qid == data.qid).all()
#                 for c in cs:
#                     if c.torf == 1:
#                         answer = c.choice
#                         return Response(response=json.dumps(answer, ensure_ascii=False))
#             # judge
#             if data.type == 6:
#                 answer = '{}'.format(session.query(qanswer).filter(qanswer.question_qid == data.qid).first().qanswer)
#                 return Response(response=json.dumps(answer, ensure_ascii=False))
#     except:
#         return Response(response=json.dumps('question id {} is not exist!'.format(qid), ensure_ascii=False),status=500)
#     session.close()
#
#
# @app.route('/getquestion/<qid>')
# @login_required
# def getquestion(qid):
#     session = DBSession()
#     data = session.query(question).filter(question.qid == qid).first()
#     data = dict(q=data.question, qid=qid, type=data.type, delornot=data.delornot, level=data.level, course=data.course)
#     print(data)
#     session.close()
#     return Response(response=json.dumps(data, ensure_ascii=False))
#
#
# @app.route('/adddati',methods=['GET','POST'])
# @login_required
# def adddati():
#     if request.method == 'POST':
#         session = DBSession()
#         answer = request.form['answer']
#         addquestion = request.form['question']
#         level = request.form['level']
#         course=request.form['course']
#
#         data=question()
#         data.question=addquestion
#         data.level=level
#         data.delornot=False
#         data.type=3
#         data.course=course
#         session.add(data)
#         session.commit()
#
#         print(data.qid)
#
#
#         addanswer=qanswer()
#         addanswer.question_qid=data.qid
#         addanswer.qanswer=answer
#         session.add(addanswer)
#         session.commit()
#
#         session.close()
#         return render_template('adddati.html',msg='add successfully!')
#     else:
#         return render_template('adddati.html')
#
#
# @app.route('/addtiankong',methods=['GET','POST'])
# @login_required
# def addtiankong():
#     if request.method == 'POST':
#         session = DBSession()
#         answer = request.form['answer']
#         addquestion = request.form['question']
#         level = request.form['level']
#         course = request.form['course']
#
#         data = question()
#         data.question = addquestion
#         data.level = level
#         data.delornot = False
#         data.type = 2
#         data.course = course
#         session.add(data)
#         session.commit()
#
#         addanswer = qanswer()
#         addanswer.question_qid = data.qid
#         addanswer.qanswer = answer
#         session.add(addanswer)
#         session.commit()
#
#         session.close()
#         return render_template('addtiankong.html', msg='add successfully!')
#     else:
#         return render_template('addtiankong.html')
#
#
# @app.route('/addchoice',methods=['GET','POST'])
# @login_required
# def addchoice():
#     if request.method == 'POST':
#         session = DBSession()
#         answer = request.form['answer']
#         wronganswer=request.form['wronganswer']
#         addquestion = request.form['question']
#         level = request.form['level']
#         course = request.form['course']
#         p1 = re.compile(r"[[](.*?)[]]", re.S)  # 最小匹配
#         answer=re.findall(p1, answer)
#         wronganswer=re.findall(p1, wronganswer)
#
#         data = question()
#         data.question = addquestion
#         data.level = level
#         data.delornot = False
#         if len(answer)==1:data.type=5
#         else:data.type=4
#         data.course = course
#         session.add(data)
#         session.commit()
#
#         for i in answer:
#             addchoice=choices(question_qid=data.qid,choice=i,torf=True)
#             session.add(addchoice)
#             session.commit()
#         for j in wronganswer:
#             addwronganswer=choices(question_qid=data.qid,choice=j,torf=False)
#             session.add(addwronganswer)
#             session.commit()
#
#         session.close()
#         return render_template('addchoice.html',msg='add successfully!')
#
#
#
#     else:
#         return render_template('addchoice.html')
#
#
# @app.route('/addjudge',methods=['GET','POST'])
# @login_required
# def addjudge():
#     if request.method == 'POST':
#         session = DBSession()
#         answer = request.form['answer']
#         addquestion = request.form['question']
#         level = request.form['level']
#         course = request.form['course']
#
#
#         data = question()
#         data.question = addquestion
#         data.level = level
#         data.delornot = False
#         data.type = 6
#         data.course = course
#         session.add(data)
#         session.commit()
#
#         addanswer=qanswer(question_qid=data.qid,qanswer=answer)
#         session.add(addanswer)
#         session.commit()
#         session.close()
#         return render_template('addjudege.html',msg='add successfully!')
#     else:
#         return render_template('addjudege.html')
#
#
# @app.route('/addjiandati',methods=['GET','POST'])
# @login_required
# def addjiandati():
#     if request.method == 'POST':
#         session = DBSession()
#         answer = request.form['answer']
#         addquestion = request.form['question']
#         level = request.form['level']
#         course=request.form['course']
#
#         data=question()
#         data.question=addquestion
#         data.level=level
#         data.delornot=False
#         data.type=1
#         data.course=course
#         session.add(data)
#         session.commit()
#
#         print(data.qid)
#
#         addanswer=qanswer()
#         addanswer.question_qid=data.qid
#         addanswer.qanswer=answer
#         session.add(addanswer)
#         session.commit()
#
#         session.close()
#         return render_template('addjiandati.html',msg='add successfully!')
#     else:
#         return render_template('addjiandati.html')
