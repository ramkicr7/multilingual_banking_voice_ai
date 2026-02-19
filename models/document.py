from extensions import db
from datetime import datetime


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    filename = db.Column(db.String(200))

    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)