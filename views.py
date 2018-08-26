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

app = Flask(__name__)
app.config['SECRET_KEY'] = '`~1!2@3#4$5%6^7&8*9(0)-_=+'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

engine = create_engine(
    'mysql+pymysql://arlen:5609651Wmm!@47.94.138.25:3306/papergenerate?charset=utf8', encoding="utf-8", echo=True,
    pool_recycle=21600, pool_size=8, max_overflow=5)
DBSession = sessionmaker(bind=engine)


@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        session=DBSession()
        email = request.form['useremail']
        username=request.form['username']
        password = request.form['userpassword']
        course=request.form['course']
        password=generate_password_hash(password)
        print(email)
        adduser=User(password=password,username=username,email=email,course=course)
        session.add(adduser)
        session.commit()

        session.close()

        return redirect(url_for('login'))
    else:
        return render_template('register.html')


@login_manager.user_loader
def load_user(user_id):
    session = DBSession()
    user = session.query(User).filter(User.userid == user_id).first()
    session.close()
    return user

@app.route('/',methods=['GET','POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            a0 = request.form['remember']
            rem = True
        except:
            rem = False
        # print(rem)
        # print(email, password)
        connect = DBSession()
        try:
            user = connect.query(User).filter(User.email == email).first()
            print(user.get_id())
            if email != '' and check_password_hash(user.password, password):
                login_user(user, remember=rem)
                return redirect(url_for('main'))
                # return render_template('main.html', user=user.username)
            else:
                return render_template('login.html', msg='login failed!')
        except:
            return render_template('login.html', msg='user {0} is not valid!'.format(email))
        connect.close()
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html', msg='You have been logout!')


@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    # load current user to class user
    user = current_user._get_current_object()
    if user.course == 0:
        privilege = 'admin'
    else:
        privilege = 'user'
    return render_template('main.html', user=user, privilege=privilege)


@app.route('/generatepage', methods=['GET', 'POST'])
@login_required
def generatepage():
    return '!!!!'


@app.route('/managepaperpage', methods=['GET', 'POST'])
@login_required
def managepaperpage():
    return '!!!!'


@app.route('/managequestionpage', methods=['GET', 'POST'])
@login_required
def managequestionpage():
    return '!!!!'


@app.route('/autogeneratepage', methods=['GET', 'POST'])
@login_required
def autogeneratepage():
    return '!!!!'


@app.route('/getusername')
@login_required
def getusername():
    cuser = current_user._get_current_object()
    data = '{}'.format(cuser.username)
    return Response(response=data)


@app.route('/getuserid')
@login_required
def getuserid():
    cuser = current_user._get_current_object()
    data = '{}'.format(cuser.userid)
    return Response(response=data)


@app.route('/getuseremail')
@login_required
def getuseremail():
    cuser = current_user._get_current_object()
    data = '{}'.format(cuser.email)
    return Response(response=data)


@app.route('/getuserprivilege')
@login_required
def getuserprivilege():
    cuser = current_user._get_current_object()
    privilege = 'user'
    if cuser.course == 0: privilege = 'admin'
    return Response(response=privilege)


@app.route('/getanswer/<qid>')
@login_required
def getanswer(qid):
    session = DBSession()
    try:
        data = session.query(question).filter(question.qid == qid).first()
        print(data)
        if data.delornot == 1:
            return 'question id is invalid!'
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
        return Response(response=json.dumps('question id {} is not exist!'.format(qid), ensure_ascii=False),status=500)
    session.close()


@app.route('/getquestion/<qid>')
@login_required
def getquestion(qid):
    session = DBSession()
    data = session.query(question).filter(question.qid == qid).first()
    data = dict(q=data.question, qid=qid, type=data.type, delornot=data.delornot, level=data.level, course=data.course)
    print(data)
    session.close()
    return Response(response=json.dumps(data, ensure_ascii=False))


@app.route('/adddati',methods=['GET','POST'])
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
        return render_template('adddati.html',msg='add successfully!')
    else:
        return render_template('adddati.html')


@app.route('/addtiankong',methods=['GET','POST'])
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
        return render_template('addtiankong.html', msg='add successfully!')
    else:
        return render_template('addtiankong.html')


@app.route('/addchoice',methods=['GET','POST'])
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
        return render_template('addchoice.html',msg='add successfully!')



    else:
        return render_template('addchoice.html')


@app.route('/addjudge',methods=['GET','POST'])
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
        return render_template('addjudege.html',msg='add successfully!')
    else:
        return render_template('addjudege.html')


@app.route('/addjiandati',methods=['GET','POST'])
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
        return render_template('addjiandati.html',msg='add successfully!')
    else:
        return render_template('addjiandati.html')





if __name__ == '__main__':
    app.run(debug=True)
