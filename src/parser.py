from src.models.models import Result
from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy()

class ResultTable():
    def insert(self, roomT):
        p=Result(roomT=roomT)
        db.session.add(p)
        db.session.commit()

    def retrieve(self, keyword=None):
        data=Result.query.all()
        #print ('data',data[0].serialize())

        return data[0].roomT