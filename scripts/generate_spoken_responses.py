import csv
import os

# ----------------------------
# BASE ANSWERS (CONTROLLED)
# ----------------------------
base_answers = {
    "balance_check": [
        "you can check your account balance using mobile banking or net banking",
        "your account balance can be viewed through the bank mobile app or net banking",
        "please use mobile banking or visit your nearest branch to know your balance"
    ],
    "debit_card_block": [
        "please block your debit card immediately using mobile banking or customer care",
        "you should block the lost debit card as soon as possible through the bank app",
        "for your safety, block the debit card immediately using available banking services"
    ],
    "upi_issue": [
        "upi issues can happen sometimes, please check your internet connection and try again",
        "you may restart the app and try the upi transaction again",
        "if the issue continues, please contact customer care or visit the branch"
    ],
    "kyc_update": [
        "to update your kyc, please visit the branch with aadhaar and pan card",
        "you can update kyc by submitting required documents at the bank branch",
        "please carry original documents for kyc verification at your nearest branch"
    ],
    "loan_info": [
        "loan details can be obtained by visiting the branch or contacting customer support",
        "you may apply for a loan by submitting the required documents at the bank",
        "bank staff will guide you regarding loan eligibility and documents"
    ]
}

# ----------------------------
# HUMAN SPEECH VARIATIONS
# ----------------------------
starters = [
    "Sure.",
    "I understand.",
    "No problem.",
    "I can help you with that.",
    "Certainly."
]

closings = [
    "",
    " Please let me know if you need further help.",
    " If you need more assistance, feel free to ask.",
    " Thank you for calling.",
    " I hope this helps."
]

# ----------------------------
# SAVE AS DATASET (CSV)
# ----------------------------
os.makedirs("data", exist_ok=True)

with open("data/spoken_answers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["intent", "answer"])

    for intent, answers in base_answers.items():
        for starter in starters:
            for answer in answers:
                for closing in closings:
                    sentence = f"{starter} {answer.capitalize()}{closing}".strip()
                    writer.writerow([intent, sentence])

print("✅ Spoken answer dataset created successfully (CSV)")
