from extensions import db
from datetime import datetime

class Loan(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    loan_type = db.Column(db.String(50))

    amount = db.Column(db.Float)
    grams = db.Column(db.Float)  # NEW
    weekly_interest = db.Column(db.Float)  # NEW

    salary = db.Column(db.Float)
    cibil_score = db.Column(db.Integer)
    purpose = db.Column(db.String(200))

    status = db.Column(db.String(20), default="Pending")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)