from flask_mail import Message
from open_science.tokens import generate_password_confirmation_token, generate_account_recovery_token, generate_email_change_token, generate_profile_delete_token
from open_science import app, mail, db
from flask import render_template, url_for
from threading import Thread
from open_science.models import EmailLog, EmailType
import datetime as dt
from sqlalchemy import func


def send_email(app, to, subject, template):
    with app.app_context():
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)


def send_email_confirmation(email):
    token = generate_password_confirmation_token(email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('email/activate_email.html',
                           confirm_url=confirm_url)
    subject = "Verify your email for OpenScience"
    Thread(target=send_email, args=(app, email, subject, html)).start()


def send_account_recovery(email):
    token = generate_account_recovery_token(email)
    set_password_url = url_for(
        'set_password_page', token=token, _external=True)
    html = render_template('email/reset_password_email.html',
                           set_password_url=set_password_url)
    subject = "Account recovery"
    Thread(target=send_email, args=(app, email, subject, html)).start()


def send_profile_delete(email):
    token = generate_profile_delete_token(email)
    delete_profile_url = url_for(
        'confirm_profile_delete', token=token, _external=True)
    html = render_template('email/delete_profile_email.html',
                           delete_profile_url=delete_profile_url)
    subject = "Deletion of the profile"
    Thread(target=send_email, args=(app, email, subject, html)).start()


def send_email_change_confirmation(email):
    token = generate_email_change_token(email)
    confirm_url = url_for('confirm_email_change', token=token, _external=True)
    html = render_template('email/change_email.html', confirm_url=confirm_url)
    subject = "Email change confirmation"
    Thread(target=send_email, args=(app, email, subject, html)).start()


def send_invite(email, first_name, second_name):
    data = {'first_name': first_name, 'second_name': second_name}
    html = render_template('email/invitation_email.html', data=data)
    subject = "Invitation for OpenScience"
    Thread(target=send_email, args=(app, email, subject, html)).start()

# TODO: use this later


def send_review_request(email, abstract, request_id):
    data = {'abstract': abstract, 'request_id': request_id}
    html = render_template('email/review_request.html', data=data)
    subject = "Review request"
    Thread(target=send_email, args=(app, email, subject, html)).start()


def insert_email_log(sender_id, reciever_id, reciever_email, email_type):
    email_log = EmailLog(sender_id, reciever_id,
                         reciever_email, dt.datetime.utcnow(), email_type)
    db.session.add(email_log)
    db.session.commit()


def get_emails_cout_last_days(sender_id, email_type_id, days):

    date_after = dt.datetime.utcnow().date() - dt.timedelta(days=days)
    count = EmailLog.query.filter(EmailLog.email_type_id == email_type_id, func.DATE(
        EmailLog.date) >= date_after, EmailLog.sender_id == sender_id).count()
    return count


def get_emails_count_to_address_last_days(reciever_email, email_type_id, days):

    date_after = dt.datetime.utcnow().date() - dt.timedelta(days=days)
    count = EmailLog.query.filter(EmailLog.email_type_id == email_type_id, func.DATE(
        EmailLog.date) >= date_after, EmailLog.receiver_email == reciever_email).count()
    return count
