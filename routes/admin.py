from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.user import User
from models.account import Account
from models.loan import Loan
from extensions import db
from services.loan_service import check_personal_loan, check_home_loan
from services.email_service import send_email

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ---------------- ADMIN DASHBOARD ----------------
@admin_bp.route("/dashboard")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        return "Access Denied"

    users = User.query.all()
    accounts = Account.query.all()

    return render_template(
        "admin/admin_dashboard.html",
        users=users,
        accounts=accounts
    )


# ---------------- FREEZE ACCOUNT ----------------
@admin_bp.route("/freeze/<int:account_id>")
@login_required
def freeze_account(account_id):

    if current_user.role != "admin":
        return "Access Denied"

    account = Account.query.get(account_id)
    account.is_frozen = True
    db.session.commit()

    return redirect(url_for("admin.admin_dashboard"))


# ---------------- UNFREEZE ACCOUNT ----------------
@admin_bp.route("/unfreeze/<int:account_id>")
@login_required
def unfreeze_account(account_id):

    if current_user.role != "admin":
        return "Access Denied"

    account = Account.query.get(account_id)
    account.is_frozen = False
    db.session.commit()

    return redirect(url_for("admin.admin_dashboard"))


# ---------------- VIEW ALL LOANS ----------------
@admin_bp.route("/loans")
@login_required
def manage_loans():

    if current_user.role != "admin":
        return "Access Denied"

    loans = Loan.query.all()
    return render_template("admin/loans.html", loans=loans)


# ---------------- APPROVE / REJECT LOAN ----------------
@admin_bp.route("/approve-loan/<int:loan_id>")
@login_required
def approve_loan(loan_id):

    if current_user.role != "admin":
        return "Access Denied"

    loan = Loan.query.get(loan_id)

    if not loan:
        return "Loan not found"

    user = User.query.get(loan.user_id)
    account = Account.query.filter_by(user_id=loan.user_id).first()

    eligible = False
    message = ""

    # ---------------- GOLD LOAN ----------------
    if loan.loan_type == "gold":
        eligible = True
        message = "Gold loan approved"

    # ---------------- PERSONAL LOAN ----------------
    elif loan.loan_type == "personal":
        eligible, message = check_personal_loan(
            loan.amount,
            loan.salary,
            loan.cibil_score
        )

    # ---------------- HOME LOAN ----------------
    elif loan.loan_type == "home":
        eligible, message = check_home_loan(
            loan.amount,
            loan.salary,
            loan.cibil_score
        )

    # ---------------- DECISION ----------------
    if eligible:
        loan.status = "Approved"

        # Credit amount to user account
        if account:
            account.balance += loan.amount

        send_email(
            user.email,
            "Loan Approved - RMBI Bank",
            f"""
Dear {user.full_name},

Your {loan.loan_type} loan of ₹{loan.amount} has been APPROVED.

The amount has been credited to your bank account.

Thank you for banking with RMBI.
"""
        )

    else:
        loan.status = "Rejected"

        send_email(
            user.email,
            "Loan Rejected - RMBI Bank",
            f"""
Dear {user.full_name},

Your {loan.loan_type} loan request has been REJECTED.

Reason:
{message}

Please contact the bank for further details.
"""
        )

    db.session.commit()

    return redirect(url_for("admin.manage_loans"))