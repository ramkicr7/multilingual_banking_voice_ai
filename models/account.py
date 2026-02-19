from extensions import db
import random

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    account_number = db.Column(db.String(20), unique=True)

    account_type = db.Column(db.String(20))  # ✅ HERE

    balance = db.Column(db.Float, default=0)

    is_frozen = db.Column(db.Boolean, default=False)

    @staticmethod
    def generate_account_number():
        return str(random.randint(100000000000, 999999999999))