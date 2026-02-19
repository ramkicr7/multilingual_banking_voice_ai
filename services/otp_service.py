import random
from datetime import datetime, timedelta
from flask import session


def generate_otp():
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    session['otp_expiry'] = (datetime.now() + timedelta(minutes=5)).isoformat()
    return otp


def verify_otp(user_otp):

    if 'otp' not in session or 'otp_expiry' not in session:
        return False

    expiry_time = datetime.fromisoformat(session['otp_expiry'])

    if datetime.now() > expiry_time:
        return False

    if user_otp != session['otp']:
        return False

    return True