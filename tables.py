from flask_sqlalchemy import Model
from sqlalchemy import *
from sqlalchemy import String, INTEGER, ForeignKey, Column, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()


class User(UserMixin,Base,Model):
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

    cid=Column(INTEGER,primary_key=true,autoincrement=True)
    choice=Column(TEXT)
    torf=Column(INTEGER)
    question_qid=Column(INTEGER,ForeignKey('question.qid'))


class qanswer(Base):
    __tablename__='qanswer'
    # qaid=Column(INTEGER,primary_key=True,autoincrement=True)
    question_qid = Column(INTEGER, ForeignKey('question.qid'),primary_key=True)
    qanswer=Column(TEXT)