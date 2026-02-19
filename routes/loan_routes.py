from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.loan import Loan
from services.loan_service import check_personal_loan, check_home_loan
from extensions import db

loan_bp = Blueprint("loan", __name__, url_prefix="/loan")


@loan_bp.route("/apply", methods=["GET", "POST"])
@login_required
def apply_loan():

    if request.method == "POST":

        loan_type = request.form["loan_type"]
        purpose = request.form["purpose"]

        # ---------------- GOLD LOAN ----------------
        if loan_type == "gold":

            grams = float(request.form["gold_weight"])
            amount = grams * 10000
            weekly_interest = amount * 0.10

            loan = Loan(
                user_id=current_user.id,
                loan_type="gold",
                amount=amount,
                grams=grams,
                weekly_interest=weekly_interest,
                salary=0,
                cibil_score=0,
                purpose=purpose,
                status="Pending"
            )

        # ---------------- PERSONAL / HOME ----------------
        else:

            amount = float(request.form["amount"])
            salary = float(request.form["salary"])
            cibil = int(request.form["cibil"])

            # Check eligibility (same as your original logic)
            if loan_type == "personal":
                eligible, message = check_personal_loan(amount, salary, cibil)
            else:
                eligible, message = check_home_loan(amount, salary, cibil)

            loan = Loan(
                user_id=current_user.id,
                loan_type=loan_type,
                amount=amount,
                salary=salary,
                cibil_score=cibil,
                purpose=purpose,
                status="Pending"
            )

        db.session.add(loan)
        db.session.commit()

        return redirect(url_for("dashboard.dashboard"))

    return render_template("loans/apply.html")