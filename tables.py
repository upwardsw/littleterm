from flask_sqlalchemy import Model
from sqlalchemy import *
from sqlalchemy import String, INTEGER, ForeignKey, Column, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

import os
Base = declarative_base()


class User(UserMixin, Base, Model):
    __tablename__ = 'user'

    userid = Column(INTEGER, primary_key=true, autoincrement=True)
    username = Column(String(16))
    email = Column(String(100))
    password = Column(String(93))
    course = Column(INTEGER)

    def get_id(self):
        return self.userid


class question(Base):
    __tablename__ = 'question'

    qid = Column(INTEGER, primary_key=true, autoincrement=True)
    question = Column(TEXT)
    type = Column(INTEGER)
    delornot = Column(INTEGER)
    level = Column(INTEGER)
    course = Column(INTEGER)

    choices = relationship('choices')
    qanswer = relationship('qanswer')


class choices(Base):
    __tablename__ = 'choices'

    cid = Column(INTEGER, primary_key=true, autoincrement=True)
    choice = Column(TEXT)
    torf = Column(INTEGER)
    question_qid = Column(INTEGER, ForeignKey('question.qid'))


class qanswer(Base):
    __tablename__ = 'qanswer'
    # qaid=Column(INTEGER,primary_key=True,autoincrement=True)
    question_qid = Column(INTEGER, ForeignKey('question.qid'), primary_key=True)
    qanswer = Column(TEXT)


class paper:
    title=0
    xuhao=0
    danxuan = []
    duoxuan = []
    pandaun = []
    jianda = []
    tiankong = []
    dati = []
    # 添加非选择题到试卷
    def addquestion(self, question):
        if question.type == 1:
            self.jianda.append(question.qid)
            return True
        if question.type == 2:
            self.tiankong.append(question.qid)
            return True
        if question.type == 3:
            self.dati.append(question.qid)
            return True
        if question.type == 6:
            self.pandaun.append(question.qid)
            return True
        else:
            return False
    # 添加单选题到试卷
    def adddanxuan(self, question):
        self.danxuan.append(question.qid)
        return True
    # 添加多选题到试卷
    def addduoxuan(self, question):
        self.duoxuan.append(question.qid)
        return True
    # 获取大题序号
    def gettitlenum(self):
        return {
            0: '一',
            1: '二',
            2: '三',
            3: '四',
            4: '五',
            5: '六',
            6: '七',
        }.get(self.title)

    def generatepaper(self,userid,filename,session):
        with open(os.getcwd() + '/static/files/{0}/{1}.txt'.format(userid,filename), 'a') as f:
            # 最后将问题写入文件并清空所有数组
            if len(self.danxuan)!=0:
                # 写入标题单选题
                title='{0},{1}'.format(self.gettitlenum(),'单选题')
                f.write('{0}\n'.format(title))
                self.title+=1
                for i in self.danxuan:
                    session.query()
            if len(self.duoxuan)!=0:
                # 写入标题多选题
                title = '{0},{1}'.format(self.gettitlenum(), '多选题')
                f.write('{0}\n'.format(title))
                self.title += 1
            if len(self.tiankong)!=0:
                # 写入标题填空题
                title = '{0},{1}'.format(self.gettitlenum(), '填空题')
                f.write('{0}\n'.format(title))
                self.title += 1
            if len(self.pandaun)!=0:
                # 写入标题判断题
                title = '{0},{1}'.format(self.gettitlenum(), '判断题')
                f.write('{0}\n'.format(title))
                self.title += 1
            if len(self.jianda)!=0:
                # 写入标题简答题
                title = '{0},{1}'.format(self.gettitlenum(), '简答题')
                f.write('{0}\n'.format(title))
                self.title += 1
            if len(self.dati)!=0:
                # 写入标题大题
                title = '{0},{1}'.format(self.gettitlenum(), '大题')
                f.write('{0}\n'.format(title))
                self.title += 1

    def writetopaper(self,userid,filename):
        pass
    # 清空试卷
    def clear(self):
        self.title=0
        self.xuhao=0
        self.tiankong=[]
        self.jianda=[]
        self.danxuan=[]
        self.duoxuan=[]
        self.pandaun=[]
        self.dati=[]

