from flask.helpers import url_for
from open_science.models import EmailLog, EmailType, Notification, Review
import datetime as dt
from sqlalchemy import func
from open_science import app, db

def delete_old_logs(days, email_type):
    date_before = dt.datetime.utcnow().date() - dt.timedelta(days = days)

    if isinstance(email_type,int):
        type_id = email_type
    else:
        type_id = EmailType.query.filter(EmailType.name==email_type).first().id

    # bulk delete
    EmailLog.query.filter(EmailLog.email_type_id==type_id,func.DATE(EmailLog.date)<date_before).delete(synchronize_session=False)
    print(f'Deleted EmailLogs. Type: {email_type}')

def create_review_deadline_notificaiton():

    date = dt.datetime.utcnow().date() + dt.timedelta(days = app.config['REVIEW_DEADLINE_REMIND'])

    reviews =  Review.query.filter(Review.deadline_date == date, Review.creation_datetime == None).all()

    for review in reviews:
        notification = Notification(Review.creator,dt.datetime.utcnow(),'2 days to expected review prepare time','review_reminder',url_for('review_edit_page',review_id=review.id))
        db.session.add(notification)

    db.session.commit() 

def monthly_jobs():
    delete_old_logs(31,'user_invite')
    
def daily_jobs():
    delete_old_logs(1,'registration_confirm')
    create_review_deadline_notificaiton()

    # , 'password change', 'email change', , 
    # 'review request', 'notification', 'staff answer',  'account delete'