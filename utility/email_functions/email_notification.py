from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
import smtplib
from .email_templates import WELCOME_MAIL_TEMPLATE
import sys
sys.path.append('')
from credentials import sender, sender_app_password

agent = smtplib.SMTP_SSL("smtp.gmail.com", 465)
agent.login(sender,sender_app_password)

def send_email(subject, content, to_addr, mail_type = 'plain' ):
    em = MIMEMultipart()
    em["From"] = sender
    em["To"] = to_addr
    em["Subject"] = subject
    em.attach(MIMEText(content, mail_type))
    agent.sendmail(sender, to_addr, em.as_string())

def send_signup_notifiction(to_addr, first_name):
    subject="Account Created at Bluelabs (noreply)"
    content= WELCOME_MAIL_TEMPLATE.format(first_name=first_name)
    send_email(to_addr=to_addr, subject=subject, content=content, mail_type='html')

def send_otp_email(to_addr, otp):
    subject="BlueLabs OPT (noreply)"
    content=f"Your OTP is: {otp}"
    send_email(to_addr=to_addr, subject=subject, content=content)