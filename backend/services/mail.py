from flask_mail import Mail, Message
from flask import current_app as app


mail = Mail()


def send_email(recipient, subject, html_body, attachment = None):
    
    msg = Message(
        subject=subject,
        sender=app.config.get('MAIL_USERNAME'),
        recipients=[recipient],
        html=html_body
    )
    
    if attachment:
        msg.attach(
            filename=attachment['filename'],
            content_type=attachment['content_type'],
            data=attachment['data']
        )

    mail.send(msg)
