from sqlalchemy.orm import backref
from src.database import db 

class Project(db.Model):
    __tablename__='project'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    results=db.relationship('Result',backref='project',lazy=True)
    
class Result(db.Model):
    __tablename__='result'

    project_id=db.Column(db.Integer,db.ForeignKey('project.id'))
    id=db.Column(db.Integer, primary_key=True)
    hour=db.Column(db.JSON,nullable=False)
    roomT=db.Column(db.JSON,nullable=False)
    clodS=db.Column(db.JSON,nullable=False)
    rhexS=db.Column(db.JSON,nullable=False)
    ahexS=db.Column(db.JSON,nullable=False)
    fs=db.Column(db.JSON,nullable=False)
    roomH=db.Column(db.JSON,nullable=False)
    clodL=db.Column(db.JSON,nullable=False)
    rhexL=db.Column(db.JSON,nullable=False)
    ahexL=db.Column(db.JSON,nullable=False)
    fl=db.Column(db.JSON,nullable=False)
    mrt=db.Column(db.JSON,nullable=False)

    def serialize(self):
        return{"room":self.roomT}