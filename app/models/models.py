from .. import db
class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voltage = db.Column(db.Float)
    current = db.Column(db.Float)
    resistance = db.Column(db.Float)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
