from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models.account import Account
from models.transaction import Transaction
from services.alert_service import send_transaction_alert

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    # Get user account
    account = Account.query.filter_by(user_id=current_user.id).first()

    if not account:
        return "Account not found"

    if request.method == "POST":

        action = request.form.get("action")
        amount = float(request.form.get("amount"))

        # Freeze check
        if account.is_frozen:
            return "Account is frozen. Contact Admin."

        # ---------------- DEPOSIT ----------------
        if action == "deposit":
            account.balance += amount

        # ---------------- WITHDRAW ----------------
        elif action == "withdraw":

            if account.balance < amount:
                return "Insufficient Balance"

            # Savings minimum balance rule
            if current_user.account_type == "savings":
                if account.balance - amount < 500:
                    return "Minimum ₹500 balance required"

            account.balance -= amount

        # Save transaction
        txn = Transaction(
            account_id=account.id,
            transaction_type=action,
            amount=amount,
            balance_after=account.balance
        )

        db.session.add(txn)
        db.session.commit()

        # Send simulated SMS alert
        send_transaction_alert(account, action, amount)

        return redirect(url_for("dashboard.dashboard"))

    # Fetch transactions
    transactions = Transaction.query.filter_by(
        account_id=account.id
    ).order_by(Transaction.timestamp.desc()).all()

    return render_template(
        "dashboard/dashboard.html",
        account=account,
        transactions=transactions
    )