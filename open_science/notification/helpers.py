from open_science.models import Notification, NotificationType, User
from open_science.enums import NotificationTypeEnum
from open_science import db
import datetime as dt
from flask.helpers import url_for
import open_science.email as em


def create_notification(type_id, text, user, action_url):
    
    notification_type = NotificationType.query.filter(
                NotificationType.id == type_id).first()
     
    notification = Notification(
        datetime=dt.datetime.utcnow(),
        title=Notification.prepare_title(type_id),
        text=text,
        action_url=action_url
    )
    notification.rel_notification_type = notification_type
    notification.rel_user = user
    db.session.add(notification)
    db.session.commit()


# TODO: add scroll to comment's div in url
def create_paper_comment_notifications(paper_revision, comment, comment_creator_id):

    # get paper creators
    paper_creators = paper_revision.rel_creators    

    # check if author is reviewer
    reviewer_commented = False

    for review in paper_revision.rel_related_reviews:
        if review.publication_datetime is not None and \
           review.creator == comment_creator_id:

            for paper_creator in paper_creators:
                create_notification(
                                    NotificationTypeEnum.REVIEWER_COMMENTED_PAPER.value,
                                    f'Reviewer commented article: {paper_revision.title}',
                                    paper_creator,
                                    url_for('article', id=paper_revision.parent_paper)
                )

                if paper_creator.is_active():
                    text = 'You have new comment from a reviewer under your paper'
                    subject = 'New comment'
                    em.send_notification_email(paper_creator.email,
                                               text,
                                               subject)
            reviewer_commented = True
            break

    if reviewer_commented is False:

        for paper_creator in paper_creators:
            create_notification(
                                NotificationTypeEnum.PAPER_COMMENT,
                                f'New comment under article: {paper_revision.title}',
                                paper_creator,
                                url_for('article', id=paper_revision.parent_paper)
            )
