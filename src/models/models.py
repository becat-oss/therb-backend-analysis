#from sqlalchemy import *

import sqlalchemy as sa
from sqlalchemy.orm import (backref,scoped_session,sessionmaker,relationship)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta
from src.config import Config
from src.database import db 
#from src.app import db

#graphql用だけどよくわかってない
engine = sa.create_engine(Config.SQLALCHEMY_DATABASE_URI,convert_unicode=True)

Base:DeclarativeMeta = declarative_base()
Base.metadata.bind = engine

db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base.query = db_session.query_property()

class Project(db.Model):
    __tablename__='project'

    id=sa.Column(sa.Integer, primary_key=True)
    name=sa.Column(sa.String,nullable=False)
    #results=relationship('Results',backref='project',lazy=True)
    therb=relationship('Therb',backref='project',lazy=True)
    kpi=relationship('Kpi',backref='project',lazy=True)

class Kpi(db.Model):
    __tablename__='kpi'
    project_id=sa.Column(sa.Integer,sa.ForeignKey('project.id'),nullable=False)
    id=sa.Column(sa.Integer, primary_key=True) 
    comfortTime=sa.Column(sa.JSON,nullable=True)
    heatLoad=sa.Column(sa.JSON,nullable=True)
    
class Therb(db.Model):#graphqlではBaseを使う
    __tablename__='therb'
    project_id=sa.Column(sa.Integer,sa.ForeignKey('project.id'),nullable=False)
    id=sa.Column(sa.Integer, primary_key=True) 
    name=sa.Column(sa.String,nullable=False) #outdoorデータのときはname=outdoor
    time=sa.Column(sa.JSON)
    temp=sa.Column(sa.JSON)
    relHumidity=sa.Column(sa.JSON)
    absHumidity=sa.Column(sa.JSON)
    sensibleLoad=sa.Column(sa.JSON,nullable=True)
    latentLoad=sa.Column(sa.JSON,nullable=True)

    def serialize(self):
        return{"room":self.temp}

    def toDict(self):
        return{
            "id":self.id,
            "name":self.name,
            "time":self.time,
            "temp":self.temp,
            "relHumidity":self.relHumidity,
            "absHumidity":self.absHumidity,
            "sensibleLoad":self.sensibleLoad,
            "latentLoad":self.latentLoad,
        }

#roomが複数ある場合のテーブル構造を考える必要あり
class Results(Base):
    #1つのroomにつき1つのResult
    __tablename__='result'

    project_id=sa.Column(sa.Integer,sa.ForeignKey('project.id'))
    id=sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=True)
    # hour=sa.Column(sa.JSON,nullable=False)
    # roomT=sa.Column(sa.JSON,nullable=False)
    # clodS=sa.Column(sa.JSON,nullable=False)
    # rhexS=sa.Column(sa.JSON,nullable=False)
    # ahexS=sa.Column(sa.JSON,nullable=False)
    # fs=sa.Column(sa.JSON,nullable=False)
    # roomH=sa.Column(sa.JSON,nullable=False)
    # clodL=sa.Column(sa.JSON,nullable=False)
    # rhexL=sa.Column(sa.JSON,nullable=False)
    # ahexL=sa.Column(sa.JSON,nullable=False)
    # fl=sa.Column(sa.JSON,nullable=False)
    # mrt=sa.Column(sa.JSON,nullable=False)

    def serialize(self):
        return{"room":self.roomT}

# Base.metadata.create_all(engine)

# class Project(db.Model):
#     __tablename__='project'

#     id=db.Column(db.Integer, primary_key=True)
#     name=db.Column(db.String,nullable=False)
#     results=sa.relationship('Result',backref='project',lazy=True)

# #roomが複数ある場合のテーブル構造を考える必要あり
# class Result(sa.Model):
#     #1つのroomにつき1つのResult
#     __tablename__='result'

#     project_id=sa.Column(sa.Integer,sa.ForeignKey('project.id'))
#     id=sa.Column(sa.Integer, primary_key=True)
#     hour=sa.Column(sa.JSON,nullable=False)
#     roomT=sa.Column(sa.JSON,nullable=False)
#     clodS=sa.Column(sa.JSON,nullable=False)
#     rhexS=sa.Column(sa.JSON,nullable=False)
#     ahexS=sa.Column(sa.JSON,nullable=False)
#     fs=sa.Column(sa.JSON,nullable=False)
#     roomH=sa.Column(sa.JSON,nullable=False)
#     clodL=sa.Column(sa.JSON,nullable=False)
#     rhexL=sa.Column(sa.JSON,nullable=False)
#     ahexL=sa.Column(sa.JSON,nullable=False)
#     fl=sa.Column(sa.JSON,nullable=False)
#     mrt=sa.Column(sa.JSON,nullable=False)

#     def serialize(self):
#         return{"room":self.roomT}