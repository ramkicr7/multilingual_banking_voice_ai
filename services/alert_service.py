def send_transaction_alert(account, action, amount):
    print(f"SMS to {account.owner.phone}")
    print(f"{action.upper()} of ₹{amount} successful.")