from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from extensions import db
from models.account import Account
from models.transaction import Transaction
from models.user import User
from services.email_service import send_email
from services.otp_service import generate_otp, verify_otp
import uuid

netbank_bp = Blueprint("netbank", __name__, url_prefix="/netbank")


# =====================================================
# STEP 1 – NETBANK LOGIN
# =====================================================
@netbank_bp.route("/login", methods=["GET", "POST"])
@login_required
def netbank_login():

    if request.method == "POST":

        nb_id = request.form.get("netbank_id")
        nb_pass = request.form.get("netbank_password")

        if nb_id != current_user.netbanking_id:
            flash("Invalid NetBanking ID")
            return redirect(url_for("netbank.netbank_login"))

        if not current_user.check_netbanking_password(nb_pass):
            flash("Invalid NetBanking Password")
            return redirect(url_for("netbank.netbank_login"))

        # Generate OTP
        otp = generate_otp()

        send_email(
            current_user.email,
            "RMBI NetBanking OTP",
            f"Your OTP for NetBanking login is {otp}. Valid for 5 minutes."
        )

        session["netbank_verified"] = False

        return redirect(url_for("netbank.netbank_otp"))

    return render_template("netbank/login.html")


# =====================================================
# STEP 2 – OTP VERIFICATION
# =====================================================
@netbank_bp.route("/otp", methods=["GET", "POST"])
@login_required
def netbank_otp():

    if request.method == "POST":

        user_otp = request.form.get("otp")

        if not verify_otp(user_otp):
            flash("Invalid or Expired OTP")
            return redirect(url_for("netbank.netbank_otp"))

        session["netbank_verified"] = True
        flash("NetBanking Login Successful")

        return redirect(url_for("netbank.netbank_dashboard"))

    return render_template("netbank/verify_otp.html")


# =====================================================
# STEP 3 – NETBANK DASHBOARD (Only Button Here)
# =====================================================
@netbank_bp.route("/dashboard")
@login_required
def netbank_dashboard():

    if not session.get("netbank_verified"):
        return redirect(url_for("netbank.netbank_login"))

    account = Account.query.filter_by(user_id=current_user.id).first()

    transactions = Transaction.query.filter_by(
        account_id=account.id
    ).order_by(Transaction.timestamp.desc()).limit(10).all()

    return render_template(
        "netbank/dashboard.html",
        account=account,
        transactions=transactions
    )


# =====================================================
# STEP 4 – TRANSFER PAGE (Separate HTML)
# =====================================================
@netbank_bp.route("/transfer-page")
@login_required
def transfer_page():

    if not session.get("netbank_verified"):
        return redirect(url_for("netbank.netbank_login"))

    account = Account.query.filter_by(user_id=current_user.id).first()

    return render_template(
        "netbank/transfer.html",
        account=account
    )


# =====================================================
# STEP 5 – PROCESS TRANSFER
# =====================================================
@netbank_bp.route("/transfer", methods=["POST"])
@login_required
def transfer_money():

    if not session.get("netbank_verified"):
        return redirect(url_for("netbank.netbank_login"))

    sender_account = Account.query.filter_by(user_id=current_user.id).first()

    receiver_account_number = request.form.get("receiver_account")
    amount = float(request.form.get("amount"))
    note = request.form.get("note", "")

    receiver_account = Account.query.filter_by(
        account_number=receiver_account_number
    ).first()

    if not receiver_account:
        flash("Receiver account not found")
        return redirect(url_for("netbank.transfer_page"))

    if sender_account.balance < amount:
        flash("Insufficient Balance")
        return redirect(url_for("netbank.transfer_page"))

    if amount <= 0:
        flash("Invalid Amount")
        return redirect(url_for("netbank.transfer_page"))

    # Unique Transaction ID
    transaction_code = str(uuid.uuid4())[:8]

    # Update balances
    sender_account.balance -= amount
    receiver_account.balance += amount

    # Create transaction entries
    sender_txn = Transaction(
        account_id=sender_account.id,
        transaction_type="transfer_sent",
        amount=amount,
        balance_after=sender_account.balance
    )

    receiver_txn = Transaction(
        account_id=receiver_account.id,
        transaction_type="transfer_received",
        amount=amount,
        balance_after=receiver_account.balance
    )

    db.session.add(sender_txn)
    db.session.add(receiver_txn)
    db.session.commit()

    # Email to Sender
    send_email(
        current_user.email,
        "Money Sent - RMBI Bank",
        f"""
Transaction Successful

Transaction ID: {transaction_code}
Amount: ₹{amount}
To Account: {receiver_account.account_number}
Note: {note}

Available Balance: ₹{sender_account.balance}
"""
    )

    # Email to Receiver
    receiver_user = db.session.get(User, receiver_account.user_id)

    send_email(
        receiver_user.email,
        "Money Received - RMBI Bank",
        f"""
Transaction Received

Transaction ID: {transaction_code}
Amount: ₹{amount}
From Account: {sender_account.account_number}
Note: {note}

Available Balance: ₹{receiver_account.balance}
"""
    )

    flash("Transfer Successful")

    return redirect(url_for("netbank.netbank_dashboard"))