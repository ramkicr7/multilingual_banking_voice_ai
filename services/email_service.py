import smtplib
from email.mime.text import MIMEText
from config import Config

def send_email(to_email, subject, body):

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = Config.MAIL_EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(Config.MAIL_EMAIL, Config.MAIL_PASSWORD)
    server.send_message(msg)
    server.quit()