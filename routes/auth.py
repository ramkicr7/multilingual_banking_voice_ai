from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models.user import User
from models.account import Account
from flask_login import login_user, logout_user, login_required
import re
import random
import string
from services.email_service import send_email

auth_bp = Blueprint("auth", __name__)


# ---------------- HOME ----------------
@auth_bp.route("/")
def home():
    return redirect(url_for("auth.login"))


# ---------------- NETBANK HELPERS ----------------
def generate_netbanking_id():
    return "NB" + ''.join(random.choices(string.digits, k=6))


def generate_netbanking_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        account_type = request.form["account_type"]
        aadhaar = request.form["aadhaar"]
        guardian_aadhaar = request.form.get("guardian_aadhaar")

        # ---------------- VALIDATIONS ----------------

        if not re.match(r"^\d{12}$", aadhaar):
            return "Invalid Aadhaar Number"

        if not re.match(r"^\d{10}$", phone):
            return "Invalid Phone Number"

        if account_type == "minor":
            if not guardian_aadhaar or not re.match(r"^\d{12}$", guardian_aadhaar):
                return "Valid Guardian Aadhaar Required"

        if User.query.filter_by(email=email).first():
            return "Email already registered"

        # ---------------- CREATE USER ----------------
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            aadhaar=aadhaar,
            role="user"
        )

        user.set_password(password)

        # -------- NETBANKING DETAILS --------
        nb_id = generate_netbanking_id()
        nb_pass = generate_netbanking_password()

        user.netbanking_id = nb_id
        user.set_netbanking_password(nb_pass)

        db.session.add(user)
        db.session.commit()

        # ---------------- CREATE BANK ACCOUNT ----------------
        account = Account(
            user_id=user.id,
            account_number=Account.generate_account_number(),
            account_type=account_type,
            balance=500 if account_type == "savings" else 0
        )

        db.session.add(account)
        db.session.commit()

        # ---------------- SEND EMAIL ----------------
        send_email(
            user.email,
            "RMBI Net Banking Credentials",
            f"""
Welcome to RMBI Bank

Your NetBanking ID: {nb_id}
Password: {nb_pass}

Please keep this secure.
"""
        )

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            login_user(user)

            if user.role == "admin":
                return redirect(url_for("admin.admin_dashboard"))

            return redirect(url_for("dashboard.dashboard"))

        return "Invalid Credentials"

    return render_template("auth/login.html")


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))