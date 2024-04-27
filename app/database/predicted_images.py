from database.database import db


class PredictedImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    
    def __init__(self, name, label, confidence):
        self.name = name
        self.label = label
        self.confidence = confidence
        