def check_personal_loan(amount, salary, cibil):
    if cibil < 650:
        return False, "Low CIBIL Score"

    if salary < amount / 10:
        return False, "Salary not sufficient"

    return True, "Eligible for Personal Loan"


def check_home_loan(amount, salary, cibil):
    if cibil < 700:
        return False, "Low CIBIL Score"

    if salary < amount / 15:
        return False, "Salary not sufficient"

    return True, "Eligible for Home Loan"