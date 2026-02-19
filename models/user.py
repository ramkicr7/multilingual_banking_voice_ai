from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):

    __tablename__ = "user"

    # ---------------- BASIC DETAILS ----------------
    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    aadhaar = db.Column(db.String(12), nullable=False)
    profile_image = db.Column(db.String(200))
    password_hash = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default="user", nullable=False)

    # ---------------- NETBANKING DETAILS ----------------
    netbanking_id = db.Column(db.String(20), unique=True, nullable=True)
    netbanking_password_hash = db.Column(db.String(200), nullable=True)

    # ---------------- RELATIONSHIPS ----------------
    accounts = db.relationship("Account", backref="owner", lazy=True)
    loans = db.relationship("Loan", backref="loan_user", lazy=True)

    # =====================================================
    # LOGIN PASSWORD METHODS
    # =====================================================
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # =====================================================
    # NETBANKING PASSWORD METHODS
    # =====================================================
    def set_netbanking_password(self, password):
        self.netbanking_password_hash = generate_password_hash(password)

    def check_netbanking_password(self, password):
        if not self.netbanking_password_hash:
            return False
        return check_password_hash(self.netbanking_password_hash, password)

    # =====================================================
    # OPTIONAL: STRING REPRESENTATION
    # =====================================================
    def __repr__(self):
        return f"<User {self.email}>"