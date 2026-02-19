from extensions import db
from datetime import datetime


class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15))
    code = db.Column(db.String(6))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)