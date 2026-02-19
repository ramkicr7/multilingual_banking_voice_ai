def apply_tax(account):
    if account.account_type == "current":
        account.balance *= 0.96  # 4% daily simulation

    if account.account_type == "savings":
        account.balance *= 0.96  # weekly simulation