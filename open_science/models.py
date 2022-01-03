from flask.helpers import url_for
from sqlalchemy import Table, DDL, event, and_
from sqlalchemy.orm import validates
from wtforms.validators import Length
from open_science.extensions import db, login_manager, bcrypt, admin
from flask_login import UserMixin
import open_science.config.models_config as mc
from open_science.db_queries import *
from open_science.admin import MyModelView, UserView, MessageToStaffView
import datetime as dt
from sqlalchemy import func
from open_science import app
from open_science.enums import UserTypeEnum, EmailTypeEnum, NotificationTypeEnum

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


association_paper_version_user = Table('association_paper_version_user', db.metadata,
                                       db.Column('paper_version_id', db.Integer, db.ForeignKey('paper_versions.id'),
                                                 primary_key=True),
                                       db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
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

association_comment_comment = Table('association_comment_comment', db.metadata,
                                    db.Column('comment_parent_id', db.Integer, db.ForeignKey('comments.id'),
                                              primary_key=True),
                                    db.Column('comment_child_id', db.Integer, db.ForeignKey('comments.id'),
                                              primary_key=True)
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

association_paper_version_license = Table('association_paper_version_license', db.metadata,
                                          db.Column('paper_version_id', db.Integer, db.ForeignKey('paper_versions.id'),
                                                    primary_key=True),
                                          db.Column('license_id', db.Integer, db.ForeignKey('licenses.id'),
                                                    primary_key=True)
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
    confirmed_on = db.Column(db.DateTime, nullable=True)
    affiliation = db.Column(db.String(length=mc.USER_AFFILIATION_L))
    orcid = db.Column(db.String(length=mc.USER_ORCID_L))
    google_scholar = db.Column(db.String(length=mc.USER_GOOGLE_SCHOLAR_L))
    about_me = db.Column(db.String(length=mc.USER_ABOUT_ME_L))
    personal_website = db.Column(db.String(length=mc.USER_PERSONAL_WEBSITE_L))
    review_mails_limit = db.Column(db.Integer(), nullable=False, default=1)
    notifications_frequency = db.Column(db.Integer(), nullable=False)
    new_email = db.Column(db.String(length=mc.USER_NEW_MAIL_L), unique=True)
    has_photo = db.Column(db.Boolean, nullable=False, default=False)
    last_seen = db.Column(db.DateTime, nullable=True)
    weight = db.Column(db.Float, nullable=False, default=1.0)
    red_flags_count = db.Column(db.Integer(), nullable=False)
    reputation = db.Column(db.Integer(), default=100, nullable=False)
    force_hide = db.Column(db.Boolean, nullable=False, default=False)
    force_show = db.Column(db.Boolean, nullable=False, default=False)

    # foreign keys
    privileges_set = db.Column(db.Integer, db.ForeignKey('privileges_sets.id'))

    # relationships
    rel_created_paper_versions = db.relationship("PaperRevision", secondary=association_paper_version_user,
                                                 back_populates="rel_creators")
    rel_tags_to_user = db.relationship("Tag", secondary=association_tag_user, back_populates="rel_users_with_this_tag")
    rel_privileges_set = db.relationship("PrivilegeSet", back_populates="rel_users")
    rel_created_tags = db.relationship("Tag", back_populates="rel_creator")
    rel_created_reviews = db.relationship("Review", back_populates="rel_creator")
    rel_created_comments = db.relationship("Comment", back_populates="rel_creator")
    rel_comment_votes_created = db.relationship("VoteComment", back_populates="rel_creator",
                                                foreign_keys="VoteComment.creator")
    rel_related_review_requests = db.relationship("ReviewRequest", back_populates="rel_requested_user")
    rel_related_staff_messages = db.relationship("MessageToStaff", back_populates="rel_sender")
    rel_comment_red_flags = db.relationship("RedFlagComment", back_populates="rel_creator",
                                            foreign_keys="RedFlagComment.creator")
    rel_paper_version_red_flags = db.relationship("RedFlagPaperVersion", back_populates="rel_creator")
    rel_review_red_flags = db.relationship("RedFlagReview", back_populates="rel_creator")
    rel_tag_red_flags = db.relationship("RedFlagTag", back_populates="rel_creator")
    rel_user_red_flags = db.relationship("RedFlagUser", back_populates="rel_creator",
                                         foreign_keys="RedFlagUser.creator")
    rel_red_flags_received = db.relationship("RedFlagUser", back_populates="rel_to_user",
                                             foreign_keys="RedFlagUser.to_user")

    # one to many, unidirectional 
    rel_notifications = db.relationship("Notification", lazy='dynamic')  # foreign_keys="Notification.user_id"

    # A 'static' variable to avoid importing the Enum class in files and use it in jinja
    user_types_enum = UserTypeEnum

    def __init__(self, first_name, second_name, email, plain_text_password, confirmed=False, confirmed_on=None,
                 affiliation="", orcid="", google_scholar="", about_me="", personal_website="", review_mails_limit=1,
                 notifications_frequency=7, photo_url="", last_seen=None, weight=1.0, registered_on=None,
                 red_flags_count=0):
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
        self.photoUrl = photo_url
        self.last_seen = last_seen
        self.weight = weight
        self.red_flags_count = red_flags_count

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    @validates('orcid')
    def set_orcid(self, key, value):
        return value.upper().replace("-","")


    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def get_new_notifications_count(self):
        return Notification.query.filter(Notification.user_id == self.id, Notification.was_seen == False).count()

    def can_request_endorsement(self, endorser_id):

        endorser_priviliege_id = db.session.query(User.privileges_set).filter_by(id=endorser_id).scalar()

        if self.id == endorser_id:
            return False

        if self.privileges_set == UserTypeEnum.STANDARD_USER.value and endorser_priviliege_id == UserTypeEnum.SCIENTIST_USER.value:
            endorsement_log = EndorsementRequestLog.query.filter(EndorsementRequestLog.user_id == self.id,
                                                                 EndorsementRequestLog.endorser_id == endorser_id).first()
            if endorsement_log:
                return False
            elif EndorsementRequestLog.get_endorsement_request_count(self.id, 1) < app.config['REQUEST_ENDORSEMENT_L']:
                return True

        return False

    def obtained_required_endorsement(self):

        if EndorsementRequestLog.get_endorsement_request_count(self.id, 365) >= app.config['ENDORSEMENT_THRESHOLD']:
            return True
        return False

    def get_orcid(self):
        return f'{self.orcid[:4]}-{self.orcid[4:8]}-{self.orcid[8:12]}-{self.orcid[12:]}'

    # TODO: change display format
    def get_google_scholar(self):
        return self.google_scholar

    def get_reviews_count(self):
        return  Review.query.filter(Review.creator==self.id,
    Review.is_hidden == False, Review.is_anonymous == False, Review.publication_datetime != None).count()
  
    def can_create_tag(self):
        if self.privileges_set >= UserTypeEnum.SCIENTIST_USER.value:
            return True
        else:
            return False
     
    def is_scientist(self):
         if self.privileges_set >= UserTypeEnum.SCIENTIST_USER.value:
             return True
         else:
            return False


class PrivilegeSet(db.Model):
    __tablename__ = "privileges_sets"

    # primary keys
    # autoincrement=False becasue ID may represent a permission level
    id = db.Column(db.Integer(), primary_key=True, autoincrement=False)

    # columns
    name = db.Column(db.String(length=mc.PS_NAME_L), nullable=False, unique=True)

    # relationships
    rel_users = db.relationship("User", back_populates="rel_privileges_set")

    def insert_types():
        for t in UserTypeEnum:
            if not PrivilegeSet.query.filter(PrivilegeSet.name == t.name).first():
                privilege_set = PrivilegeSet(id = t.value, name=t.name)
                db.session.add(privilege_set)
        db.session.commit()

    def __repr__(self):
        return f'<PrivilegeSet {self.id} {self.name}>'


class Tag(db.Model):
    __tablename__ = "tags"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    # uppercase letters and digits (.isalnum())
    name = db.Column(db.String(length=mc.TAG_NAME_L), nullable=False, unique=True)
    description = db.Column(db.String(length=mc.TAG_DESCRIPTION_L), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    red_flags_count = db.Column(db.Integer(), default=0, nullable=False)
    force_hide = db.Column(db.Boolean, nullable=False, default=False)
    force_show = db.Column(db.Boolean, nullable=False, default=False)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_related_paper_versions = db.relationship("PaperRevision", secondary=association_tag_paper_version,
                                                 back_populates="rel_related_tags")
    rel_users_with_this_tag = db.relationship("User", secondary=association_tag_user, back_populates="rel_tags_to_user")
    rel_creator = db.relationship("User", back_populates="rel_created_tags")
    rel_red_flags_received = db.relationship("RedFlagTag", back_populates="rel_to_tag")

    @validates('name')
    def convert_upper(self, key, value):
        return value.upper()


class Paper(db.Model):
    __tablename__ = "papers"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # relationships
    rel_related_versions = db.relationship("PaperRevision", back_populates="rel_parent_paper")

    def get_latest_revision(self):
       return max(self.rel_related_versions, key = lambda v: v.publication_date)

    # TODO: I think this new dict conversion will be better and should maintain backwards compatibility
    # However, in case of problems just uncomment the old version below
    # def to_dict(self):
    #     return {
    #         'id': self.id
    #     }
    def to_dict(self):
        return {
            'id': self.id,
            'paper_title': self.get_latest_revision().title,
            'publication_datetime': self.get_latest_revision().publication_date
        }



class CalibrationPaper(db.Model):

    __tablename__ = "calibration_papers"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    pdf_url = db.Column(db.String(mc.PV_PDF_URL_L), nullable=False)
    preprocessed_text = db.Column(db.Text(), nullable=True)

     #foreign keys
    author = db.Column(db.Integer, db.ForeignKey('users.id'))



class PaperRevision(db.Model):
    __tablename__ = "paper_versions"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    version = db.Column(db.Integer(), default=1, nullable=False)
    pdf_url = db.Column(db.String(mc.PV_PDF_URL_L), nullable=False)
    title = db.Column(db.String(length=mc.PV_TITLE_L), nullable=False)
    abstract = db.Column(db.String(length=mc.PV_ABSTRACT_L), nullable=False)
    summarized_changes = db.Column(db.String(length=mc.PV_CHANGES_L), nullable=True)
    publication_date = db.Column(db.DateTime)
    confidence_level = db.Column(db.SmallInteger(), default=0, nullable=False)
    red_flags_count = db.Column(db.Integer(), default=0, nullable=False)
    # is blank if no anonymous version exists
    anonymized_pdf_url = db.Column(db.String(mc.PV_PDF_URL_L), nullable=True)
    force_hide = db.Column(db.Boolean, nullable=False, default=False)
    force_show = db.Column(db.Boolean, nullable=False, default=False)

    #preprocessed text
    preprocessed_text = db.Column(db.Text(), nullable=True)

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
    rel_creators = db.relationship("User", secondary=association_paper_version_user,
                                   back_populates="rel_created_paper_versions")
    rel_related_licenses = db.relationship("License", secondary=association_paper_version_license,
                                           back_populates="rel_related_paper_versions")
    rel_red_flags_received = db.relationship("RedFlagPaperVersion", back_populates="rel_to_paper_version")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'publication_date': self.publication_date
        }

    def get_active_reviews_list(self):
        return [review for review in self.rel_related_reviews if review.publication_datetime is not None]

    def get_missing_reviews_count(self):
        return max(0, self.confidence_level - len(self.get_active_reviews_list()))


class Review(db.Model):
    __tablename__ = "reviews"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    weight = db.Column(db.Float, nullable=True)
    text = db.Column(db.String(mc.REVIEW_TEXT_L), nullable=True)
    review_score = db.Column(db.Integer(), nullable=True)
    # datetime of review's submission
    publication_datetime = db.Column(db.DateTime, nullable=True)
    # deadline of submitting review
    deadline_date = db.Column(db.Date, nullable=True)
    red_flags_count = db.Column(db.Integer(), nullable=False, default=0)
    edit_counter = db.Column(db.Integer(), nullable=False, default=0)
    is_anonymous = db.Column(db.Boolean, nullable=False, default=False)
    is_hidden = db.Column(db.Boolean, nullable=False, default=False)
    force_hide = db.Column(db.Boolean, nullable=False, default=False)
    force_show = db.Column(db.Boolean, nullable=False, default=False)

    # evaluation criteria
    evaluation_novel = db.Column(db.Float(precision=2), nullable=False, default=0.0)
    evaluation_conclusion = db.Column(db.Float(precision=2), nullable=False, default=0.0)
    evaluation_error = db.Column(db.Float(precision=2), nullable=False, default=0.0)
    evaluation_organize = db.Column(db.Float(precision=2), nullable=False, default=0.0)
    confidence = db.Column(db.Float(precision=2), nullable=False, default=0.0)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    related_paper_version = db.Column(db.Integer, db.ForeignKey('paper_versions.id'))

    # relationships
    rel_comments_to_this_review = db.relationship("Comment", secondary=association_comment_review,
                                                  back_populates="rel_related_review")
    rel_creator = db.relationship("User", back_populates="rel_created_reviews")
    rel_related_paper_version = db.relationship("PaperRevision", back_populates="rel_related_reviews")
    rel_red_flags_received = db.relationship("RedFlagReview", back_populates="rel_to_review")

    def get_paper_title(self):
        return db.session.query(PaperRevision.title).filter(
            PaperRevision.id == self.related_paper_version).scalar()

    def to_dict(self):
        return {
            'id': self.id,
            'paper_title': self.get_paper_title(),
            'publication_datetime': self.publication_datetime,
            'edit_url': url_for('review_edit_page', review_id=self.id)
        }

    def get_author_name(self):
        names = db.session.query(User.first_name,User.second_name).filter(User.id==self.rel_creator.id).first()
        print(names)
        return f'{names[0]} {names[1]}'

    def is_published(self):
        return self.publication_datetime != None

    # returns reviews connected to previous paper versions
    def get_previous_reviews(self):
        paper_versions = self.rel_related_paper_version.rel_parent_paper.rel_related_versions
        previous_paper_versions = [version for version in paper_versions
                                   if version.version < self.rel_related_paper_version.version]
        previous_reviews = []
        for version in previous_paper_versions:
            for review in version.rel_related_reviews:
                previous_reviews.append(review)

        return previous_reviews

    # returns reviews connected to previous paper versions written by self.creator
    def get_previous_creator_reviews(self):
        paper_versions = self.rel_related_paper_version.rel_parent_paper.rel_related_versions
        previous_paper_versions = [version for version in paper_versions
                                   if version.version < self.rel_related_paper_version.version]
        previous_reviews = []
        for version in previous_paper_versions:
            for review in version.rel_related_reviews:
                if review.creator == self.creator:
                    previous_reviews.append(review)

        return previous_reviews

class ReviewRequest(db.Model):
    __tablename__ = "review_requests"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    decision = db.Column(db.Boolean, nullable=True)
    creation_datetime = db.Column(db.DateTime)
    acceptation_date = db.Column(db.Date)
    # deadline of showing request
    deadline_date = db.Column(db.Date)

    # decilne reasons
    reason_conflict_interest = db.Column(db.Boolean, nullable=False, default=False)
    reason_lack_expertise = db.Column(db.Boolean, nullable=False, default=False)
    reason_time = db.Column(db.Boolean, nullable=False, default=False)
    reason_match_incorrectly = db.Column(db.Boolean, nullable=False, default=False)

    reason_other = db.Column(db.Boolean, nullable=False, default=False)
    other_reason_text = db.Column(db.String(length=mc.DR_REASON_L), nullable=True)

    # foreign keys
    requested_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    paper_version = db.Column(db.Integer, db.ForeignKey('paper_versions.id'))

    # relationships
    rel_requested_user = db.relationship("User", back_populates="rel_related_review_requests")
    rel_related_paper_version = db.relationship("PaperRevision", back_populates="rel_related_review_requests")

    def set_reasons(self, reason_ids):

        # not elegant solution
        for id in reason_ids:
            if id == 0:
                self.reason_conflict_interest = True
            elif id == 1:
                self.reason_lack_expertise = True
            elif id == 2:
                self.reason_time = True
            elif id == 3:
                self.reason_match_incorrectly = True
            elif id == 4:
                self.reason_other = True



class Comment(db.Model):
    __tablename__ = "comments"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    text = db.Column(db.String(length=mc.COMMENT_TEXT_L))
    votes_score = db.Column(db.Integer(), nullable=False)
    red_flags_count = db.Column(db.Integer(), nullable=False)
    level = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.DateTime)
    force_hide = db.Column(db.Boolean, nullable=False, default=False)
    force_show = db.Column(db.Boolean, nullable=False, default=False)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_related_paper_version = db.relationship("PaperRevision", secondary=association_comment_paper_version,
                                                back_populates="rel_related_comments")
    rel_related_review = db.relationship("Review", secondary=association_comment_review,
                                         back_populates="rel_comments_to_this_review")
    rel_related_comment = db.relationship("Comment",
                                          secondary=association_comment_comment,
                                          primaryjoin=association_comment_comment.c.comment_parent_id == id,
                                          secondaryjoin=association_comment_comment.c.comment_child_id == id,
                                          back_populates="rel_comments_to_this_comment")
    rel_comments_to_this_comment = db.relationship("Comment",
                                                   secondary=association_comment_comment,
                                                   primaryjoin=association_comment_comment.c.comment_child_id == id,
                                                   secondaryjoin=association_comment_comment.c.comment_parent_id == id,
                                                   back_populates="rel_related_comment")
    rel_creator = db.relationship("User", back_populates="rel_created_comments")
    rel_comment_votes_received = db.relationship("VoteComment", back_populates="rel_to_comment")
    rel_red_flags_received = db.relationship("RedFlagComment", back_populates="rel_to_comment",
                                             foreign_keys="RedFlagComment.to_comment")


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

    reasons = ('Conflict of interest', 'Lack of expertise', 'Don’t have time', 'Paper matched incorrectly', 'Other')

    def insert_reasons():
        for t in DeclinedReason.reasons:
            if not DeclinedReason.query.filter(DeclinedReason.reason == t).first():
                reason = DeclinedReason(reason=t)
                db.session.add(reason)
        db.session.commit()

    def __repr__(self):
        return f'<DeclinedReason {self.id} {self.reason}>'


class MessageTopic(db.Model):
    __tablename__ = "message_topics"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    topic = db.Column(db.String(length=mc.MT_TOPIC_L), nullable=False)

    # relationships
    rel_related_staff_messages = db.relationship("MessageToStaff", back_populates="rel_topic")

    topics = ('Endorsement', 'Technical issues, corrections', 'Other')

    def insert_topics():
        for t in MessageTopic.topics:
            if not MessageTopic.query.filter(MessageTopic.topic == t).first():
                message_topic = MessageTopic(topic=t)
                db.session.add(message_topic)
        db.session.commit()

    def __repr__(self):
        return f'<MessageTopic {self.id} {self.topic}>'


class EmailType(db.Model):
    __tablename__ = 'email_types'
    # primary keys
    id = db.Column(db.Integer(), primary_key=True)
    # columns
    name = db.Column(db.String(length=mc.EM_TYPE_NAME_L), nullable=False, unique=True)
    rel_email_logs = db.relationship("EmailLog")

    def insert_types():
        for t in EmailTypeEnum:
            if not EmailType.query.filter(EmailType.name == t.name).first():
                email_type = EmailType(id = t.value, name=t.name)
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
    receiver_id = db.Column(db.Integer, nullable=True)
    receiver_email = db.Column(db.String(length=mc.USER_EMAIL_L), nullable=False)
    date = db.Column(db.DateTime, nullable=True)

    # foreign keys
    email_type_id = db.Column(db.Integer, db.ForeignKey('email_types.id'))

    email_types_enum = EmailTypeEnum

    def __init__(self, sender_id, reciever_id, reciever_email, date, email_type):
        self.sender_id = sender_id
        self.receiver_id = reciever_id
        self.receiver_email = reciever_email
        self.date = date
        if isinstance(email_type, int):
            self.email_type_id = email_type
        else:
            self.email_type_id = EmailType.query.filter(EmailType.name == email_type).one().id


class NotificationType(db.Model):
    __tablename__ = 'notification_types'

    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    name = db.Column(db.String(length=mc.EM_TYPE_NAME_L), nullable=False, unique=True)
    rel_email_logs = db.relationship("Notification")

    def insert_types():
        for t in NotificationTypeEnum:
            if not NotificationType.query.filter(NotificationType.name == t.name).first():
                notification_type = NotificationType(id = t.value, name=t.name)
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
    datetime = db.Column(db.DateTime, nullable=True)
    title = db.Column(db.String(length=mc.NOTIFICATION_TITLE_L), nullable=False)
    text = db.Column(db.String(length=mc.NOTIFICATION_TEXT_L), nullable=False)
    action_url = db.Column(db.String(length=mc.NOTIFICATION_ACTION_URL_L), nullable=True)
    was_seen = db.Column(db.Boolean, nullable=False, default=False)

    # foreign keys
    notification_type_id = db.Column(db.Integer, db.ForeignKey('notification_types.id'))

    notification_types_enum = NotificationTypeEnum

    def __init__(self, user_id, datetime, text, notification_type, action_url=''):
        self.user_id = user_id
        self.datetime = datetime
        self.text = text
        self.action_url = action_url
        self.set_title(notification_type)

        if isinstance(notification_type, int):
            self.notification_type_id = notification_type
        else:
            self.notification_type_id = db.session.query(NotificationType.id).filter(
                NotificationType.name == notification_type).one().id

    def set_title(self, notification_type):
        if isinstance(notification_type, str):
            type_string = notification_type
        else:
            type_string = db.session.query(NotificationType.name).filter(
                NotificationType.id == notification_type).one().name

        self.title = type_string.replace('_', ' ').lower().capitalize()


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


class RedFlagComment(db.Model):
    __tablename__ = "red_flags_comment"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_comment = db.Column(db.Integer, db.ForeignKey('comments.id'))

    # relationships
    rel_creator = db.relationship("User", back_populates="rel_comment_red_flags", foreign_keys=[creator])
    rel_to_comment = db.relationship("Comment", back_populates="rel_red_flags_received", foreign_keys=[to_comment])


class RedFlagPaperVersion(db.Model):
    __tablename__ = "red_flags_paper_version"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_paper_version = db.Column(db.Integer, db.ForeignKey('paper_versions.id'))

    # relationships
    rel_creator = db.relationship("User", back_populates="rel_paper_version_red_flags")
    rel_to_paper_version = db.relationship("PaperRevision", back_populates="rel_red_flags_received")


class RedFlagReview(db.Model):
    __tablename__ = "red_flags_review"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_review = db.Column(db.Integer, db.ForeignKey('reviews.id'))

    # relationships
    rel_creator = db.relationship("User", back_populates="rel_review_red_flags")
    rel_to_review = db.relationship("Review", back_populates="rel_red_flags_received")


class RedFlagTag(db.Model):
    __tablename__ = "red_flags_tag"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_tag = db.Column(db.Integer, db.ForeignKey('tags.id'))

    # relationships
    rel_creator = db.relationship("User", back_populates="rel_tag_red_flags")
    rel_to_tag = db.relationship("Tag", back_populates="rel_red_flags_received")


class RedFlagUser(db.Model):
    __tablename__ = "red_flags_user"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_creator = db.relationship("User", back_populates="rel_user_red_flags", foreign_keys=[creator])
    rel_to_user = db.relationship("User", back_populates="rel_red_flags_received", foreign_keys=[to_user])


class License(db.Model):
    __tablename__ = "licenses"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    license = db.Column(db.String(length=mc.L_LICENSE_L), nullable=False)

    # relationships
    rel_related_paper_versions = db.relationship("PaperRevision", secondary=association_paper_version_license,
                                                 back_populates="rel_related_licenses")


class EndorsementRequestLog(db.Model):
    __tablename__ = "endorsement_request_logs"

    # columns
    decision = db.Column(db.Boolean(), default=False, nullable=False)
    date = db.Column(db.Date(), nullable=False)
    considered = db.Column(db.Boolean(), default=False, nullable=False)

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    endorser_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def get_endorsement_request_count(user_id, days):
        date_after = dt.datetime.utcnow().date() - dt.timedelta(days=days)
        count = EndorsementRequestLog.query.filter(EndorsementRequestLog.user_id == user_id,
                                                   func.DATE(EndorsementRequestLog.date) > date_after,
                                                   EndorsementRequestLog.decision == True).count()
        return count


# db functions
db_fun_update_comment_score = DDL(q_update_comment_score)

# db triggers
db_trig_update_comment_score = DDL(qt_update_comment_score)

# events to enable functions, procedures, triggers etc
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

admin.add_view(MessageToStaffView(MessageToStaff, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(MyModelView(PaperRevision, db.session))
admin.add_view(MyModelView(Tag, db.session))
admin.add_view(MyModelView(Review, db.session))
admin.add_view(MyModelView(ReviewRequest, db.session))
admin.add_view(MyModelView(Comment, db.session))


def create_essential_data():
    PrivilegeSet.insert_types()
    DeclinedReason.insert_reasons()
    MessageTopic.insert_topics()
    EmailType.insert_types()
    NotificationType.insert_types()

    # site as user to log emails send from site and use ForeignKey in EmailLog model
    # confirmed=False hides user
    if not User.query.filter(User.id == 0).first():
        user_0 = User(
            first_name="site",
            second_name="site",
            email="open.science.mail@gmail.com",
            plain_text_password="QWerty12#$%^&*()jumbo",
            confirmed=False,
            review_mails_limit=0,
            notifications_frequency=0,
        )
        user_0.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.STANDARD_USER.value).first()
        user_0.id = 0
        db.session.add(user_0)

    db.session.commit()
    print("The essential data has been created")

    return True
