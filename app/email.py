from flask_mail import Message
from .config import Config
from .extensions import mail

def send_email(to, subject, template):
    '''sends email'''
    msg = Message(
        recipients=[to],
        subject=subject,
        html=template,
        sender= Config.MAIL_DEFAULT_SENDER
    )
    mail.send(msg)
