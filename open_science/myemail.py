from flask_mail import Message
from open_science.tokens import generate_password_confirmation_token, \
                                generate_account_recovery_token, \
                                generate_email_change_token, \
                                generate_profile_delete_token
from open_science import  mail, db
from flask import current_app
from flask import render_template, url_for
from threading import Thread
from open_science.models import EmailLog
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
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('email/activate_email.html',
                           confirm_url=confirm_url)
    subject = "Verify your account at Researcher.community"
    Thread(target=send_email, args=(current_app._get_current_object(), email, subject, html)).start()


def send_account_recovery(email):
    token = generate_account_recovery_token(email)
    set_password_url = url_for(
        'auth.set_password_page', token=token, _external=True)
    html = render_template('email/reset_password_email.html',
                           set_password_url=set_password_url)
    subject = "Account recovery for Researcher.community"
    Thread(target=send_email, args=(current_app._get_current_object(), email, subject, html)).start()


def send_profile_delete(email):
    token = generate_profile_delete_token(email)
    delete_profile_url = url_for(
        'auth.confirm_profile_delete', token=token, _external=True)
    html = render_template('email/delete_profile_email.html',
                           delete_profile_url=delete_profile_url)
    subject = "Deletion of the profile at Researcher.community"
    Thread(target=send_email, args=(current_app._get_current_object(), email, subject, html)).start()


def send_email_change_confirmation(email):
    token = generate_email_change_token(email)
    confirm_url = url_for('auth.confirm_email_change', token=token, _external=True)
    html = render_template('email/change_email.html', confirm_url=confirm_url)
    subject = "Email address change confirmation at Researcher.community"
    Thread(target=send_email, args=(current_app._get_current_object(), email, subject, html)).start()


def send_invite(email, first_name, second_name):
    data = {'first_name': first_name, 'second_name': second_name}
    html = render_template('email/invitation_email.html', data=data)
    subject = "Invitation to join Researcher.community"
    Thread(target=send_email, args=(current_app._get_current_object(), email, subject, html)).start()


def send_review_request(email, abstract, request_id):
    data = {'abstract': abstract, 'request_id': request_id}
    html = render_template('email/review_request_email.html', data=data)
    subject = "Review request from Researcher.community"
    Thread(target=send_email, args=(current_app._get_current_object(), email, subject, html)).start()


def send_new_review_notification(email, review_id, paper_title):
    data = {'review_id': review_id, 'paper_title': paper_title}
    html = render_template('email/new_review_email.html', data=data)
    subject = "New paper review at Researcher.community"
    Thread(target=send_email, args=(current_app._get_current_object(), email, subject, html)).start()


def insert_email_log(sender_id, reciever_id, reciever_email, email_type_id):
    email_log = EmailLog(sender_id, reciever_id,
                         reciever_email, dt.datetime.utcnow(), email_type_id)
    db.session.add(email_log)
    db.session.commit()


# from sender
def get_emails_cout_last_days(sender_id, email_type_id, days):

    date_after = dt.datetime.utcnow().date() - dt.timedelta(days=days)
    count = EmailLog.query \
        .filter(EmailLog.email_type_id == email_type_id,
                func.DATE(EmailLog.date) >= date_after,
                EmailLog.sender_id == sender_id) \
        .count()
    return count


# to reciever
def get_emails_count_to_address_last_days(reciever_email,
                                          email_type_id,
                                          days=10000):

    date_after = dt.datetime.utcnow().date() - dt.timedelta(days=days)
    count = EmailLog.query.filter(EmailLog.email_type_id == email_type_id,
                                  func.DATE(
                                            EmailLog.date) >= date_after,
                                  EmailLog.receiver_email == reciever_email) \
        .count()
    return count


def send_notification_email(email, text, subject):
    data = {'text': text}
    html = render_template('email/notification_email.html', data=data)
    Thread(target=send_email, args=(current_app._get_current_object(), email, subject, html)).start()
