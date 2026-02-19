import pandas as pd
import random

intents = {
    "balance_check": [
        "check my balance", "tell me my balance", "what is my account balance",
        "balance enquiry", "show my balance"
    ],
    "mini_statement": [
        "show my mini statement", "last 5 transactions", "recent transactions",
        "mini statement please", "transaction history"
    ],
    "loan_info": [
        "loan details", "how to apply for loan", "loan eligibility",
        "documents needed for loan", "loan interest details"
    ],
    "upi_issue": [
        "UPI is not working", "UPI payment failed", "UPI transaction pending",
        "UPI issue", "UPI not responding"
    ],
    "kyc_update": [
        "update my KYC", "KYC update process", "how to update KYC",
        "KYC documents", "KYC verification"
    ]
}

prefixes = ["", "Hi,", "Hello,", "Sir,", "Please", "Kindly", "I want to", "Can you", "Help me to"]
suffixes = ["", "please", "now", "today", "immediately", "as soon as possible"]

data = []

for intent, phrases in intents.items():
    for _ in range(200):  # 200 per intent
        phrase = random.choice(phrases)
        sent = f"{random.choice(prefixes)} {phrase} {random.choice(suffixes)}"
        sent = " ".join(sent.split())
        data.append([sent, intent])

df = pd.DataFrame(data, columns=["sentence", "intent"])
df.to_csv("data/intents_en.csv", index=False)

print("✅ intents_en.csv created successfully!")
