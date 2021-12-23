from enum import unique
from sqlalchemy import Table, DDL, event
from sqlalchemy.orm import validates
from sqlalchemy.sql.functions import user
from wtforms.validators import Email

from open_science.extensions import db, login_manager, bcrypt, admin

from flask_login import UserMixin
import datetime as dt

import open_science.config.models_config as mc
from open_science.db_queries import *
from open_science.admin import MyModelView, UserView, MessageToStaffView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


association_paper_user = Table('association_paper_user', db.metadata,
                               db.Column('paper_id', db.Integer, db.ForeignKey('papers.id'), primary_key=True),
                               db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
                               )

association_comment_post = Table('association_comment_post', db.metadata,
                                 db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'), primary_key=True),
                                 db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
                                 )

association_comment_paper_version = Table('association_comment_paper_version', db.metadata,
                                          db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'),
                                                    primary_key=True),
                                          db.Column('paper_version_id', db.Integer, db.ForeignKey('paper_versions.id'),
                                                    primary_key=True)
                                          )

association_comment_review = Table('association_comment_review', db.metadata,
                                   db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'), primary_key=True),
                                   db.Column('review_id', db.Integer, db.ForeignKey('reviews.id'), primary_key=True)
                                   )

association_tag_paper_version = Table('association_tag_paper_version', db.metadata,
                                      db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
                                      db.Column('paper_version_id', db.Integer, db.ForeignKey('paper_versions.id'),
                                                primary_key=True)
                                      )

association_tag_user = Table('association_tag_user', db.metadata,
                             db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
                             db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
                             )


class User(db.Model, UserMixin):
    __tablename__ = "users"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    first_name = db.Column(db.String(length=mc.USER_FIRST_NAME_L), nullable=False)
    second_name = db.Column(db.String(length=mc.USER_SECOND_NAME_L), nullable=False)
    email = db.Column(db.String(length=mc.USER_EMAIL_L), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=mc.USER_PASS_HASH_L), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime,nullable=True)
    affiliation = db.Column(db.String(length=mc.USER_AFFILIATION_L))
    orcid = db.Column(db.String(length=mc.USER_ORCID_L))
    google_scholar = db.Column(db.String(length=mc.USER_GOOGLE_SCHOLAR_L))
    about_me = db.Column(db.String(length=mc.USER_ABOUT_ME_L))
    personal_website = db.Column(db.String(length=mc.USER_PERSONAL_WEBSITE_L))
    review_mails_limit = db.Column(db.Integer(), nullable=False, default=1)
    notifications_frequency = db.Column(db.Integer(), nullable=False)
    votes_score = db.Column(db.Integer(), nullable=False, default=100)
    new_email = db.Column(db.String(length=mc.USER_NEW_MAIL_L), unique=True)
    has_photo = db.Column(db.Boolean, nullable=False, default=False)
    last_seen = db.Column(db.DateTime, nullable=True)
    weight = db.Column(db.Float, nullable=False, default=1.0)
 

    # foreign keys
    privileges_set = db.Column(db.Integer, db.ForeignKey('privileges_sets.id'))

    # relationships
    rel_created_papers = db.relationship("Paper", secondary=association_paper_user, back_populates="rel_creators")
    rel_tags_to_user = db.relationship("Tag", secondary=association_tag_user, back_populates="rel_users_with_this_tag")
    rel_privileges_set = db.relationship("PrivilegeSet", back_populates="rel_users")
    rel_created_tags = db.relationship("Tag", back_populates="rel_creator")
    rel_created_reviews = db.relationship("Review", back_populates="rel_creator")
    rel_created_comments = db.relationship("Comment", back_populates="rel_creator")
    rel_created_posts = db.relationship("Post", back_populates="rel_creator")
    rel_user_votes_received = db.relationship("VoteUser", back_populates="rel_to_user",
                                              foreign_keys="VoteUser.to_user")
    rel_user_votes_created = db.relationship("VoteUser", back_populates="rel_creator",
                                             foreign_keys="VoteUser.creator")
    rel_paper_votes_created = db.relationship("VotePaper", back_populates="rel_creator",
                                              foreign_keys="VotePaper.creator")
    rel_review_votes_created = db.relationship("VoteReview", back_populates="rel_creator",
                                               foreign_keys="VoteReview.creator")
    rel_comment_votes_created = db.relationship("VoteComment", back_populates="rel_creator",
                                                foreign_keys="VoteComment.creator")
    rel_post_votes_created = db.relationship("VotePost", back_populates="rel_creator",
                                             foreign_keys="VotePost.creator")
    rel_related_review_requests = db.relationship("ReviewRequest", back_populates="rel_requested_user")
    rel_related_staff_messages = db.relationship("MessageToStaff", back_populates="rel_sender")

    # one to many, unidirectional 
    rel_notifications = db.relationship("Notification",lazy='dynamic') # foreign_keys="Notification.user_id"

    def __init__(self, first_name, second_name, email, plain_text_password, confirmed=False, confirmed_on=None,
                 affiliation="", orcid="", google_scholar="", about_me="", personal_website="", review_mails_limit=1,
                 notifications_frequency=7, votes_score=100, photo_url="", last_seen=None, weight=1.0,
                 registered_on=None):
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self.password = plain_text_password
        self.registered_on = registered_on
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.affiliation = affiliation
        self.orcid = orcid
        self.google_scholar = google_scholar
        self.about_me = about_me
        self.personal_website = personal_website
        self.review_mails_limit = review_mails_limit
        self.notifications_frequency = notifications_frequency
        self.votes_score = votes_score
        self.photoUrl = photo_url
        self.last_seen = last_seen
        self.weight = weight

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def get_new_notifications_count(self):
        return Notification.query.filter(Notification.user_id==self.id, Notification.was_seen==False).count()
            


class PrivilegeSet(db.Model):
    __tablename__ = "privileges_sets"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    name = db.Column(db.String(length=mc.PS_NAME_L), nullable=False, unique=True)

    # relationships
    rel_users = db.relationship("User", back_populates="rel_privileges_set")

    types = ('standard_user', 'scientific_user','admin')

    def insert_types():
        for t in PrivilegeSet.types:
             if not PrivilegeSet.query.filter(PrivilegeSet.name==t).first():
                privilege_set = PrivilegeSet(name=t)
                db.session.add(privilege_set)
        db.session.commit()
    
    def __repr__(self):
        return f'<PrivilegeSet {self.id} {self.name}>'

class Tag(db.Model):
    __tablename__ = "tags"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    name = db.Column(db.String(length=mc.TAG_NAME_L), nullable=False, unique=True)
    description = db.Column(db.String(length=mc.TAG_DESCRIPTION_L))
    deadline = db.Column(db.DateTime)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_related_paper_versions = db.relationship("PaperVersion", secondary=association_tag_paper_version,
                                                 back_populates="rel_related_tags")
    rel_users_with_this_tag = db.relationship("User", secondary=association_tag_user, back_populates="rel_tags_to_user")
    rel_creator = db.relationship("User", back_populates="rel_created_tags")

    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()


class Paper(db.Model):
    __tablename__ = "papers"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    license = db.Column(db.String(length=mc.PAPER_LICENSE_L))
    confidence_level = db.Column(db.SmallInteger(), default=0, nullable=False)
    votes_score = db.Column(db.Integer(), default=0, nullable=False)

    # relationships
    rel_creators = db.relationship("User", secondary=association_paper_user, back_populates="rel_created_papers")
    rel_paper_votes_received = db.relationship("VotePaper", back_populates="rel_to_paper")
    rel_related_versions = db.relationship("PaperVersion", back_populates="rel_parent_paper")

    def to_dict(self):
        return {
            'id': self.id,
            'license': self.license,
            'confidence_level': self.confidence_level,
            'votes_score': self.votes_score
        }


class PaperVersion(db.Model):
    __tablename__ = "paper_versions"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    version = db.Column(db.Integer(),default = 1,nullable=False)
    pdf_url = db.Column(db.String(mc.PV_PDF_URL_L), nullable=False)
    title = db.Column(db.String(length=mc.PV_TITLE_L), nullable=False)
    abstract = db.Column(db.String(length=mc.PV_ABSTRACT_L), nullable=False)
    publication_date = db.Column(db.DateTime)

    # foreign keys
    parent_paper = db.Column(db.Integer, db.ForeignKey('papers.id'))

    # relationships
    rel_related_comments = db.relationship("Comment", secondary=association_comment_paper_version,
                                           back_populates="rel_related_paper_version")
    rel_related_tags = db.relationship("Tag", secondary=association_tag_paper_version,
                                       back_populates="rel_related_paper_versions")
    rel_related_reviews = db.relationship("Review", back_populates="rel_related_paper_version")
    rel_parent_paper = db.relationship("Paper", back_populates="rel_related_versions")
    rel_related_review_requests = db.relationship("ReviewRequest", back_populates="rel_related_paper_version")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'publication_date': self.publication_date
        }


class Review(db.Model):
    __tablename__ = "reviews"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    weight = db.Column(db.Float, nullable=True)
    text = db.Column(db.String(mc.REVIEW_TEXT_L),nullable=True)
    votes_score = db.Column(db.Integer(), nullable=True)
    review_score = db.Column(db.Integer(), nullable=True)
    creation_datetime = db.Column(db.DateTime,nullable=True)
    deadline_date = db.Column(db.Date,nullable=True)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    related_paper_version = db.Column(db.Integer, db.ForeignKey('paper_versions.id'))

    # relationships
    rel_comments_to_this_review = db.relationship("Comment", secondary=association_comment_review,
                                                  back_populates="rel_related_review")
    rel_creator = db.relationship("User", back_populates="rel_created_reviews")
    rel_related_paper_version = db.relationship("PaperVersion", back_populates="rel_related_reviews")
    rel_review_votes_received = db.relationship("VoteReview", back_populates="rel_to_review")


class ReviewRequest(db.Model):
    __tablename__ = "review_requests"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    decision = db.Column(db.Boolean, nullable=False, default=False)
    creation_datetime = db.Column(db.DateTime)
    acceptation_date = db.Column(db.Date)
    deadline_date = db.Column(db.Date)

    # foreign keys
    declined_reason = db.Column(db.Integer, db.ForeignKey('declined_reasons.id'))
    requested_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    paper_version = db.Column(db.Integer, db.ForeignKey('paper_versions.id'))

    # relationships
    rel_declined_reason = db.relationship("DeclinedReason", back_populates="rel_related_review_requests")
    rel_requested_user = db.relationship("User", back_populates="rel_related_review_requests")
    rel_related_paper_version = db.relationship("PaperVersion", back_populates="rel_related_review_requests")


class Comment(db.Model):
    __tablename__ = "comments"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    text = db.Column(db.String(length=mc.COMMENT_TEXT_L))
    votes_score = db.Column(db.Integer(), nullable=False)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_related_post = db.relationship("Post", secondary=association_comment_post,
                                       back_populates="rel_comments_to_this_post")
    rel_related_paper_version = db.relationship("PaperVersion", secondary=association_comment_paper_version,
                                                back_populates="rel_related_comments")
    rel_related_review = db.relationship("Review", secondary=association_comment_review,
                                         back_populates="rel_comments_to_this_review")
    rel_creator = db.relationship("User", back_populates="rel_created_comments")
    rel_comment_votes_received = db.relationship("VoteComment", back_populates="rel_to_comment")


class Post(db.Model):
    __tablename__ = "posts"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    text = db.Column(db.String(length=mc.POST_TEXT_L))
    votes_score = db.Column(db.Integer(), nullable=False)
    red_flags_count = db.Column(db.Integer(), nullable=False)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_comments_to_this_post = db.relationship("Comment", secondary=association_comment_post,
                                                back_populates="rel_related_post")
    rel_creator = db.relationship("User", back_populates="rel_created_posts")
    rel_post_votes_received = db.relationship("VotePost", back_populates="rel_to_post")


class MessageToStaff(db.Model):
    __tablename__ = "messages_to_staff"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    text = db.Column(db.String(length=mc.MTS_TEXT_L), nullable=False)
    date = db.Column(db.DateTime)
    replied = db.Column(db.Boolean, nullable=False, default=False)

    # foreign keys
    sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic = db.Column(db.Integer, db.ForeignKey('message_topics.id'))

    # relationships
    rel_sender = db.relationship("User", back_populates="rel_related_staff_messages")
    rel_topic = db.relationship("MessageTopic", back_populates="rel_related_staff_messages")


class DeclinedReason(db.Model):
    __tablename__ = "declined_reasons"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    reason = db.Column(db.String(length=mc.DR_REASON_L), nullable=False)

    # relationships
    rel_related_review_requests = db.relationship("ReviewRequest", back_populates="rel_declined_reason")

    reasons = ("Conflict of interest","Lack of expertise","Don’t have time","Paper matched incorrectly","Other")

    def insert_reasons():
        for t in DeclinedReason.reasons:
             if not DeclinedReason.query.filter(DeclinedReason.reason==t).first():
                reason = DeclinedReason(reason=t)
                db.session.add(reason)
        db.session.commit()
      



class MessageTopic(db.Model):
    __tablename__ = "message_topics"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    topic = db.Column(db.String(length=mc.MT_TOPIC_L), nullable=False)

    # relationships
    rel_related_staff_messages = db.relationship("MessageToStaff", back_populates="rel_topic")

    def __repr__(self):
        return f'<MessageTopic {self.id} {self.topic}>'

    topics = ('Endorsement','Technical issues, corrections', 'Other' )
    def insert_topics():
        for t in MessageTopic.topics:
             if not MessageTopic.query.filter(MessageTopic.topic==t).first():
                message_topic = MessageTopic(topic=t)
                db.session.add(message_topic)
        db.session.commit()


class EmailType(db.Model):
    __tablename__ = 'email_types'
    # primary keys
    id = db.Column(db.Integer(), primary_key=True)
    # columns
    name = db.Column(db.String(length=mc.EM_TYPE_NAME_L),nullable=False,unique=True)
    rel_email_logs = db.relationship("EmailLog")

    # types
    types = ('registration_confirm', 'password_change', 'email_change', 'user_invite', 
    'review_request', 'notification', 'staff_answer',  'account_delete')

    def insert_types():
        for t in EmailType.types:
             if not EmailType.query.filter(EmailType.name==t).first():
                email_type = EmailType(name=t)
                db.session.add(email_type)
        db.session.commit()
      
    def __repr__(self):
        return f'<EmailType {self.id} {self.name}>'

class EmailLog(db.Model):
    __tablename__ = 'email_logs'
    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer,nullable=True)
    receiver_email = db.Column(db.String(length=mc.USER_EMAIL_L), nullable=False)
    date = db.Column(db.DateTime,nullable=True)

    # foreign keys
    email_type_id = db.Column(db.Integer, db.ForeignKey('email_types.id'))

    def __init__(self,sender_id,reciever_id,reciever_email,date,email_type):
        self.sender_id = sender_id
        self.receiver_id = reciever_id
        self.receiver_email = reciever_email
        self.date = date
        if isinstance(email_type,int):
            self.email_type_id = email_type
        else:
            self.email_type_id = EmailType.query.filter(EmailType.name==email_type).one().id



class NotificationType(db.Model):
    __tablename__ = 'notification_types'
    # primary keys
    id = db.Column(db.Integer(), primary_key=True)
    # columns
    name = db.Column(db.String(length=mc.EM_TYPE_NAME_L),nullable=False,unique=True)
    rel_email_logs = db.relationship("Notification")

    # types
    types = ('review_request', 'new_review', 'comment_answer', 'review_answer', 'system_message')

    def insert_types():
        for t in NotificationType.types:
             if not NotificationType.query.filter(NotificationType.name==t).first():
                notification_type = NotificationType(name=t)
                db.session.add(notification_type)
        db.session.commit()
          
    def __repr__(self):
        return f'<NotificationType {self.id} {self.name}>'

class Notification(db.Model):
    __tablename__ = 'notifications'
    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    datetime = db.Column(db.DateTime,nullable=True)
    title = db.Column(db.String(length=mc.NOTIFICATION_TITLE_L), nullable=False)
    text = db.Column(db.String(length=mc.NOTIFICATION_TEXT_L), nullable=False)
    action_url = db.Column(db.String(length=mc.NOTIFICATION_ACTION_URL_L), nullable=False)
    was_seen =  db.Column(db.Boolean,nullable=False, default=False)
    # foreign keys
    notification_type_id = db.Column(db.Integer, db.ForeignKey('notification_types.id'))

    def __init__(self,user_id, datetime, text, action_url, notification_type):
        self.user_id = user_id
        self.datetime = datetime
        self.text = text
        self.action_url = action_url
        self.set_title(notification_type)

        if isinstance(notification_type,int):
            self.notification_type_id = notification_type
        else:
            self.notification_type_id = db.session.query(NotificationType.id).filter(NotificationType.name==notification_type).one().id

    def set_title(self, notification_type):
        if isinstance(notification_type,str):
            type_string = notification_type
        else:
            type_string =  db.session.query(NotificationType.name).filter(NotificationType.id==notification_type).one().name
        
        self.title = type_string.replace('_',' ').capitalize()

class VoteUser(db.Model):
    __tablename__ = "votes_users"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    is_up = db.Column(db.Boolean, nullable=False)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_creator = db.relationship("User", back_populates="rel_user_votes_created", foreign_keys=[creator])
    rel_to_user = db.relationship("User", back_populates="rel_user_votes_received", foreign_keys=[to_user])


class VotePaper(db.Model):
    __tablename__ = "votes_papers"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    is_up = db.Column(db.Boolean, nullable=False)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_paper = db.Column(db.Integer, db.ForeignKey('papers.id'))

    # relationships
    rel_creator = db.relationship("User", back_populates="rel_paper_votes_created")
    rel_to_paper = db.relationship("Paper", back_populates="rel_paper_votes_received")


class VoteReview(db.Model):
    __tablename__ = "votes_reviews"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    is_up = db.Column(db.Boolean, nullable=False)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_review = db.Column(db.Integer, db.ForeignKey('reviews.id'))

    # relationships
    rel_creator = db.relationship("User", back_populates="rel_review_votes_created")
    rel_to_review = db.relationship("Review", back_populates="rel_review_votes_received")


class VoteComment(db.Model):
    __tablename__ = "votes_comments"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    is_up = db.Column(db.Boolean, nullable=False)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_comment = db.Column(db.Integer, db.ForeignKey('comments.id'))

    # relationships
    rel_creator = db.relationship("User", back_populates="rel_comment_votes_created")
    rel_to_comment = db.relationship("Comment", back_populates="rel_comment_votes_received")


class VotePost(db.Model):
    __tablename__ = "votes_posts"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    is_up = db.Column(db.Boolean, nullable=False)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_post = db.Column(db.Integer, db.ForeignKey('posts.id'))

    # relationships
    rel_creator = db.relationship("User", back_populates="rel_post_votes_created", foreign_keys=creator)
    rel_to_post = db.relationship("Post", back_populates="rel_post_votes_received", foreign_keys=to_post)


# db functions
db_fun_update_user_score = DDL(q_update_user_score)
db_fun_update_paper_score = DDL(q_update_paper_score)
db_fun_update_review_score = DDL(q_update_review_score)
db_fun_update_comment_score = DDL(q_update_comment_score)
db_fun_update_post_score = DDL(q_update_post_score)

# db triggers
db_trig_update_user_score = DDL(qt_update_user_score)
db_trig_update_paper_score = DDL(qt_update_paper_score)
db_trig_update_review_score = DDL(qt_update_review_score)
db_trig_update_comment_score = DDL(qt_update_comment_score)
db_trig_update_post_score = DDL(qt_update_post_score)

# events to enable functions, procedures, triggers etc
event.listen(
    VoteUser.__table__,
    'after_create',
    db_fun_update_user_score.execute_if(dialect='postgresql')
)

event.listen(
    VoteUser.__table__,
    'after_create',
    db_trig_update_user_score.execute_if(dialect='postgresql')
)

event.listen(
    VotePaper.__table__,
    'after_create',
    db_fun_update_paper_score.execute_if(dialect='postgresql')
)

event.listen(
    VotePaper.__table__,
    'after_create',
    db_trig_update_paper_score.execute_if(dialect='postgresql')
)

event.listen(
    VoteReview.__table__,
    'after_create',
    db_fun_update_review_score.execute_if(dialect='postgresql')
)

event.listen(
    VoteReview.__table__,
    'after_create',
    db_trig_update_review_score.execute_if(dialect='postgresql')
)

event.listen(
    VoteComment.__table__,
    'after_create',
    db_fun_update_comment_score.execute_if(dialect='postgresql')
)

event.listen(
    VoteComment.__table__,
    'after_create',
    db_trig_update_comment_score.execute_if(dialect='postgresql')
)

event.listen(
    VotePost.__table__,
    'after_create',
    db_fun_update_post_score.execute_if(dialect='postgresql')
)

event.listen(
    VotePost.__table__,
    'after_create',
    db_trig_update_post_score.execute_if(dialect='postgresql')
)

admin.add_view(MessageToStaffView(MessageToStaff, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(MyModelView(Paper, db.session))
admin.add_view(MyModelView(PaperVersion, db.session))
admin.add_view(MyModelView(Tag, db.session))
admin.add_view(MyModelView(Review, db.session))
admin.add_view(MyModelView(ReviewRequest, db.session))
admin.add_view(MyModelView(Comment, db.session))

