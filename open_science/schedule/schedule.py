from re import L
from flask.helpers import url_for
from open_science.enums import NotificationTypeEnum, EmailTypeEnum
from open_science.models import EmailLog, EmailType, Review, User, Paper
import datetime as dt
from sqlalchemy import func
from open_science import app, db
from open_science.notification.helpers import create_notification
import open_science.email as em
from open_science.review.helpers import prepare_review_requests
import text_processing.similarity_matrix as sm
from text_processing.plot import create_save_users_plot

def delete_old_logs(days, email_type):
    date_before = dt.datetime.utcnow().date() - dt.timedelta(days=days)

    if isinstance(email_type, int):
        type_id = email_type
    else:
        type_id = EmailType.query.filter(
            EmailType.name == email_type).first().id

    # bulk delete
    EmailLog.query \
        .filter(EmailLog.email_type_id == type_id,
                func.DATE(EmailLog.date) < date_before) \
        .delete(synchronize_session=False)

    print(f'Deleted EmailLogs. Type: {email_type}')


def create_review_deadline_notification():
    date = dt.datetime.utcnow().date() + \
        dt.timedelta(days=app.config['REVIEW_DEADLINE_REMIND'])

    reviews = Review.query.filter(
        Review.deadline_date == date, Review.publication_datetime.is_(None)) \
        .all()

    for review in reviews:
        create_notification(
                    NotificationTypeEnum.REVIEW_REMINDER.value,
                    '2 days to expected review prepare time',
                    review.creator,
                    url_for('review_edit_page', review_id=review.id)
                )

    db.session.commit()


def send_notifiactions_count():

    all_users = User.query.filter(User.confirmed.is_(True)).all()

    for user in all_users:
        if user.is_active() and user.notifications_frequency > 0:
            count = user.get_new_notifications_count()
            if count != 0:
                last_emails = em.get_emails_count_to_address_last_days(
                    user.email,
                    EmailTypeEnum.NOTIFICATION.value,
                    user.notifications_frequency
                )
                if last_emails == 0:
                    text = f'You have {count} unread notifications on your profile'
                    subject = 'New notifications'

                    em.send_notification_email(user.email,
                                               text,
                                               subject)


def prepare_and_send_review_requests():
    papers = Paper.query.all()
    for paper in papers:
        paper_revision = paper.get_latest_revision()
        prepare_review_requests(paper_revision)


def monthly_jobs():
    delete_old_logs(31, EmailLog.email_types_enum.USER_INVITE.value)


def daily_jobs():
    dictionary = sm.create_dictionary()
    sm.save_dictionary(dictionary)
    tfidf_matrix = sm.create_tfidf_matrix()
    sm.save_tfidf_matrix(tfidf_matrix)
    similarities_matrix = sm.create_similarities_matrix()
    sm.save_similarities_matrix(similarities_matrix)
    create_save_users_plot()

    delete_old_logs(2, EmailLog.email_types_enum.REGISTRATION_CONFIRM.value)
    create_review_deadline_notification()
    send_notifiactions_count()
    prepare_and_send_review_requests()
    