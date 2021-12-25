from open_science.models import EmailLog, EmailType
import datetime as dt
from sqlalchemy import func

def delete_old_logs(days, email_type):
    date_before = dt.datetime.utcnow().date() - dt.timedelta(days = days)

    if isinstance(email_type,int):
        type_id = email_type
    else:
        type_id = EmailType.query.filter(EmailType.name==email_type).first().id

    # bulk delete
    EmailLog.query.filter(EmailLog.email_type_id==type_id,func.DATE(EmailLog.date)<date_before).delete(synchronize_session=False)
    print(f'Deleted EmailLogs. Type: {email_type}')

def monthly_jobs():
    delete_old_logs(31,'user_invite')
    
def daily_jobs():
    delete_old_logs(1,'registration_confirm')
    
    # , 'password change', 'email change', , 
    # 'review request', 'notification', 'staff answer',  'account delete'