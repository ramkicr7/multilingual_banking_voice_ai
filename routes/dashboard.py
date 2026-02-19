from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from extensions import db
from models.account import Account
from models.transaction import Transaction
import os
from services.email_service import send_email
from services.otp_service import generate_otp, verify_otp

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    account = Account.query.filter_by(user_id=current_user.id).first()

    if not account:
        return "Account not found"

    if request.method == "POST":

        action = request.form.get("action")
        amount = float(request.form.get("amount"))

        if account.is_frozen:
            return "Account is frozen by Admin"

        # Store temporarily
        session["pending_action"] = action
        session["pending_amount"] = amount

        # Generate OTP
        otp = generate_otp()

        message = f"Your OTP for {action} of ₹{amount} is {otp}. Valid for 5 minutes."

        send_email(
            current_user.email,
            "RMBI Bank OTP Verification",
            message
        )

        flash("OTP sent to your registered email")
        return redirect(url_for("dashboard.verify_otp_page"))

    transactions = Transaction.query.filter_by(
        account_id=account.id
    ).order_by(Transaction.timestamp.desc()).all()

    return render_template(
        "dashboard/dashboard.html",
        account=account,
        transactions=transactions
    )


@dashboard_bp.route("/verify-otp")
@login_required
def verify_otp_page():
    return render_template("dashboard/verify_otp.html")


@dashboard_bp.route("/verify-otp", methods=["POST"])
@login_required
def verify_otp_route():

    account = Account.query.filter_by(user_id=current_user.id).first()

    user_otp = request.form.get("otp")

    if not verify_otp(user_otp):
        flash("Invalid or Expired OTP")
        return redirect(url_for("dashboard.verify_otp_page"))

    action = session.get("pending_action")
    amount = session.get("pending_amount")

    if action == "deposit":
        account.balance += amount

    elif action == "withdraw":

        if account.balance < amount:
            return "Insufficient Balance"

        if account.account_type == "savings":
            if account.balance - amount < 500:
                return "Minimum ₹500 balance required"

        account.balance -= amount

    txn = Transaction(
        account_id=account.id,
        transaction_type=action,
        amount=amount,
        balance_after=account.balance
    )

    db.session.add(txn)
    db.session.commit()

    # Confirmation Email
    send_email(
        current_user.email,
        "Transaction Successful - RMBI Bank",
        f"₹{amount} {action} successful. Available balance ₹{account.balance}."
    )

    # Clear session
    session.clear()

    flash("Transaction Successful")
    return redirect(url_for("dashboard.dashboard"))
# -----------------------------------
# UPLOAD PROFILE PHOTO
# -----------------------------------
@dashboard_bp.route("/upload-photo", methods=["POST"])
@login_required
def upload_photo():

    file = request.files.get("photo")

    if not file:
        flash("No file selected")
        return redirect(url_for("dashboard.dashboard"))

    # Create folder if not exists
    upload_folder = os.path.join("static", "profile_pics")
    os.makedirs(upload_folder, exist_ok=True)

    filename = f"user_{current_user.id}.png"
    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    current_user.profile_image = filename
    db.session.commit()

    flash("Profile photo updated successfully")
    return redirect(url_for("dashboard.dashboard"))