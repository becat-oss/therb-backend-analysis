from src.database import db 

class Result(db.Model):
    __tablename__='result'

    id=db.Column(db.Integer, primary_key=True)
    roomT=db.Column(db.JSON,nullable=False)

    def serialize(self):
        return{"room":self.roomT}