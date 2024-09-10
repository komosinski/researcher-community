from flask.helpers import url_for
from flask import Markup
from sqlalchemy import Table, DDL, event, Sequence
from sqlalchemy.orm import validates
from operator import and_, or_
from flask_login import UserMixin
import config.models_config as mc
import datetime as dt
from sqlalchemy import func
from config.auto_endorse_config import EMAIL_REGEXPS
import re
import text_processing.search_engine as se

from flask import current_app as app

from open_science.db_badge_triggers import b_first_article_award_function, b_first_comment_award_function, \
    b_first_article_award_trigger, b_first_comment_award_trigger
# ImportError, use current_app instead
# from open_science import app

from open_science.enums import UserTypeEnum, EmailTypeEnum, \
    NotificationTypeEnum, MessageTopicEnum
from open_science.db_queries import q_update_comment_score, q_update_user_red_flags_count, q_update_tag_red_flags_count, \
    q_update_review_red_flags_count, q_update_user_reputation, q_update_revision_red_flags_count, \
    q_update_comment_red_flags_count, q_update_revision_averages, qt_update_comment_score, qt_update_user_reputation, \
    qt_update_user_red_flags_count, qt_update_tag_red_flags_count, qt_update_review_red_flags_count, \
    qt_update_revision_red_flags_count, qt_update_comment_red_flags_count, qt_update_revision_averages
from open_science.extensions import db, login_manager, bcrypt
from open_science.licenses import LICENSE_DICT


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


association_paper_version_user = Table('association_paper_version_user', db.metadata,
                                       db.Column('paper_version_id', db.Integer, db.ForeignKey('paper_revisions.id'),
                                                 primary_key=True),
                                       db.Column('user_id', db.Integer, db.ForeignKey(
                                           'users.id'), primary_key=True),
                                       )

association_comment_paper_version = Table('association_comment_paper_version', db.metadata,
                                          db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'),
                                                    primary_key=True),
                                          db.Column('paper_version_id', db.Integer, db.ForeignKey('paper_revisions.id'),
                                                    primary_key=True)
                                          )

association_comment_review = Table('association_comment_review', db.metadata,
                                   db.Column('comment_id', db.Integer, db.ForeignKey(
                                       'comments.id'), primary_key=True),
                                   db.Column('review_id', db.Integer, db.ForeignKey(
                                       'reviews.id'), primary_key=True)
                                   )

association_comment_comment = Table('association_comment_comment', db.metadata,
                                    db.Column('comment_parent_id', db.Integer, db.ForeignKey('comments.id'),
                                              primary_key=True),
                                    db.Column('comment_child_id', db.Integer, db.ForeignKey('comments.id'),
                                              primary_key=True)
                                    )

association_comment_forum_topic = Table('association_comment_forum_topic', db.metadata,
                                   db.Column('comment_id', db.Integer, db.ForeignKey(
                                       'comments.id'), primary_key=True),
                                   db.Column('forum_topic_id', db.Integer, db.ForeignKey(
                                       'forum_topics.id'), primary_key=True)
                                   )

association_tag_paper_version = Table('association_tag_paper_version', db.metadata,
                                      db.Column('tag_id', db.Integer, db.ForeignKey(
                                          'tags.id'), primary_key=True),
                                      db.Column('paper_version_id', db.Integer, db.ForeignKey('paper_revisions.id'),
                                                primary_key=True)
                                      )

association_paper_version_license = Table('association_paper_version_license', db.metadata,
                                          db.Column('paper_version_id', db.Integer, db.ForeignKey('paper_revisions.id'),
                                                    primary_key=True),
                                          db.Column('license_id', db.Integer, db.ForeignKey('licenses.id'),
                                                    primary_key=True)
                                          )

# Association with extra data pattern: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-object
class AssociationTagUser(db.Model):
    __tablename__ = "association_tag_user"
    tag_id = db.Column(db.ForeignKey("tags.id"), primary_key=True)
    user_id = db.Column(db.ForeignKey("users.id"), primary_key=True)
    # parent user who appointed tag with user
    appointer_id = db.Column(db.Integer, nullable=False)

    can_appoint = db.Column(db.Boolean, default=False)
    can_edit = db.Column(db.Boolean, default=False)

    rel_user = db.relationship("User", back_populates="assoc_tags_to_user")
    rel_tag = db.relationship("Tag", back_populates="assoc_users_with_this_tag")


class User(db.Model, UserMixin):
    __tablename__ = "users"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True)

    # columns
    first_name = db.Column(
        db.String(length=mc.USER_FIRST_NAME_L), nullable=False)
    second_name = db.Column(
        db.String(length=mc.USER_SECOND_NAME_L), nullable=False)
    email = db.Column(db.String(length=mc.USER_EMAIL_L),
                      nullable=False, unique=True)
    password_hash = db.Column(
        db.String(length=mc.USER_PASS_HASH_L), nullable=False)

    # Empty if user is not registered paper's co-author
    registered_on = db.Column(db.DateTime, nullable=True)

    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    affiliation = db.Column(db.String(length=mc.USER_AFFILIATION_L))
    orcid = db.Column(db.String(length=mc.USER_ORCID_L))
    google_scholar = db.Column(db.String(length=mc.USER_GOOGLE_SCHOLAR_L))
    about_me = db.Column(db.String(length=mc.USER_ABOUT_ME_L))
    personal_website = db.Column(db.String(length=mc.USER_PERSONAL_WEBSITE_L))
    review_mails_limit = db.Column(db.Integer(), nullable=False, default=0)
    notifications_frequency = db.Column(db.Integer(), nullable=False)

    # Holds a new email address before being validated or information
    # about attempt to delete account 'DELETE_PROFILE_ATTEMPT'
    new_email = db.Column(db.String(length=mc.USER_NEW_MAIL_L), unique=True)

    has_photo = db.Column(db.Boolean, nullable=False, default=False)
    last_seen = db.Column(db.DateTime, nullable=True)
    weight = db.Column(db.Float, nullable=False, default=1.0)
    red_flags_count = db.Column(db.Integer(), nullable=False, default=0)
    reputation = db.Column(db.Integer(), default=100, nullable=False)
    force_hide = db.Column(db.Boolean, nullable=False, default=False)
    force_show = db.Column(db.Boolean, nullable=False, default=False)

    # Field only visible to administrators. Store issues related to account
    remarks = db.Column(db.String(length=mc.USER_REMARKS_L), nullable=True)

    is_deleted = db.Column(db.Boolean, nullable=True)

    # foreign keys
    privileges_set = db.Column(db.Integer, db.ForeignKey('privileges_sets.id'))

    # relationships
    rel_created_paper_revisions = db.relationship("PaperRevision", secondary=association_paper_version_user,
                                                  back_populates="rel_creators")
    rel_privileges_set = db.relationship(
        "PrivilegeSet", back_populates="rel_users")
    rel_created_tags = db.relationship("Tag", back_populates="rel_creator")
    rel_created_reviews = db.relationship(
        "Review", back_populates="rel_creator")
    rel_created_comments = db.relationship(
        "Comment", back_populates="rel_creator")
    rel_comment_votes_created = db.relationship("VoteComment", back_populates="rel_creator",
                                                foreign_keys="VoteComment.creator")
    rel_related_review_requests = db.relationship(
        "ReviewRequest", back_populates="rel_requested_user")
    rel_related_staff_messages = db.relationship(
        "MessageToStaff", back_populates="rel_sender")
    rel_comment_red_flags = db.relationship("RedFlagComment", back_populates="rel_creator",
                                            foreign_keys="RedFlagComment.creator")
    rel_paper_version_red_flags = db.relationship(
        "RedFlagPaperRevision", back_populates="rel_creator")
    rel_review_red_flags = db.relationship(
        "RedFlagReview", back_populates="rel_creator")
    rel_tag_red_flags = db.relationship(
        "RedFlagTag", back_populates="rel_creator")
    rel_user_red_flags = db.relationship("RedFlagUser", back_populates="rel_creator",
                                         foreign_keys="RedFlagUser.creator")
    rel_red_flags_received = db.relationship("RedFlagUser", back_populates="rel_to_user",
                                             foreign_keys="RedFlagUser.to_user")
    rel_calibration_papers = db.relationship(
        "CalibrationPaper", back_populates="rel_author")
    rel_notifications = db.relationship(
        "Notification", back_populates="rel_user", lazy='dynamic')

    rel_user_badges = db.relationship('UserBadge', backref='user', lazy=True)

    assoc_tags_to_user = db.relationship("AssociationTagUser", back_populates="rel_user")

    # A 'static' variable to avoid importing the Enum class in files and use it in jinja
    user_types_enum = UserTypeEnum

    def __init__(self, first_name, second_name, email, plain_text_password, confirmed=False, confirmed_on=None,
                 affiliation="", orcid="", google_scholar="", about_me="", personal_website="", review_mails_limit=1,
                 notifications_frequency=7, last_seen=None, weight=1.0, registered_on=None,
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
        return value.upper().replace("-", "")

    @validates('google_scholar')
    def set_google_scholar(self, key, value):
        return value.replace("https://scholar.google.com/", "")

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash,
                                          attempted_password)

    def get_new_notifications_count(self):
        return Notification.query.filter(Notification.user == self.id, Notification.was_seen.is_(False)).count()

    def can_request_endorsement(self, endorser_id):

        endorser_priviliege_id = db.session.query(
            User.privileges_set).filter_by(id=endorser_id).scalar()

        if self.id == endorser_id:
            return False

        if self.privileges_set == UserTypeEnum.STANDARD_USER.value and \
                endorser_priviliege_id == UserTypeEnum.RESEARCHER_USER.value:
            endorsement_log = EndorsementRequestLog \
                .query.filter(
                    EndorsementRequestLog.user_id == self.id,
                    EndorsementRequestLog.endorser_id == endorser_id) \
                .first()
            if endorsement_log:
                return False
            elif EndorsementRequestLog. \
                    get_endorsement_request_count(self.id, 1) \
                    < app.config['REQUEST_ENDORSEMENT_L']:
                return True

        return False

    def obtained_required_endorsement(self):

        if EndorsementRequestLog.get_endorsement_request_count(self.id, 365) \
                >= app.config['ENDORSEMENT_THRESHOLD']:
            return True
        return False

    def get_orcid(self):
        return f'{self.orcid[:4]}-{self.orcid[4:8]}-\
            {self.orcid[8:12]}-{self.orcid[12:]}'

    # TODO: change display format
    def get_google_scholar(self):
        return self.google_scholar

    def get_reviews_count(self):
        return Review.query.filter(Review.creator == self.id,
                                   and_(or_(Review.force_show.is_(True),
                                            Review.red_flags_count
                                            < app.config['RED_FLAGS_THRESHOLD']),
                                        Review.force_hide.is_(False)),
                                   Review.is_anonymous.is_(False),
                                   Review.publication_datetime != None) \
            .count()

    def can_create_tag(self):
        count = Tag.query.filter(Tag.creator == self.id,
                                 Tag.creation_date == dt.datetime.utcnow()
                                 .date()) \
            .count()
        if self.privileges_set >= UserTypeEnum.RESEARCHER_USER.value \
                and count < app.config['TAGS_L']:
            return True
        else:
            return False

    def is_researcher(self):
        if self.privileges_set >= UserTypeEnum.RESEARCHER_USER.value:
            return True
        else:
            return False

    def is_admin(self):
        if self.privileges_set >= UserTypeEnum.ADMIN.value:
            return True
        else:
            return False

    def is_standard_user(self):
        if self.privileges_set == UserTypeEnum.STANDARD_USER.value:
            return True
        else:
            return False

    def endorse(self):
        if self.privileges_set < UserTypeEnum.RESEARCHER_USER.value:
            self.rel_privileges_set = PrivilegeSet.query.filter(
                PrivilegeSet.id == User.user_types_enum.RESEARCHER_USER.value) \
                .first()
            db.session.commit()

    def try_endorse_with_email(self):
        if self.privileges_set < UserTypeEnum.RESEARCHER_USER.value:
            for regex in EMAIL_REGEXPS:
                if re.search(regex, self.email):
                    self.endorse()
                    return True
        return False

    def get_similar_users_ids(self):
        similar_ids = []

        all_users = User.query.all()
        users_dict_id = {}
        for user in all_users:
            if user.id != 0:
                users_dict_id[user.id] = [revision.id for revision in user.rel_created_paper_revisions]

        similar_ids = se.get_similar_users_to_user(self.id, users_dict_id)

        return similar_ids

    def get_similar_users(self):
        similar_users = []

        similar_users_ids = self.get_similar_users_ids()
        similar_users = User.query.filter(User.id.in_(similar_users_ids)) \
            .paginate().items

        return similar_users

    # confirmed, not deleted etc
    def is_active(self):
        if self.confirmed is True and self.is_deleted is not True:
            return True
        else:
            return False

    def get_review_workload(self):
        count = 0
        days = app.config['REVIEWER_WORKLOAD_ON_DAYS']
        date_after = dt.datetime.utcnow().date() - dt.timedelta(days=days)
        for rev_request in self.rel_related_review_requests:
            if rev_request.decision is True \
                    and rev_request.response_date >= date_after:
                count += 1
        return count

    def get_current_review_mails_limit(self):
        count = 0
        days_after = dt.datetime.utcnow() - dt.timedelta(days=30)
        for rev_request in self.rel_related_review_requests:
            if rev_request.creation_datetime >= days_after:
                count += 1
        return max(0, self.review_mails_limit - count)

    def delete_profile(self):
        self.first_name = 'Deleted'
        self.second_name = 'user'
        self.is_deleted = True
        self.force_hide = True
        self.affiliation = None
        self.orcid = ''
        self.google_scholar = ''
        self.about_me = None
        self.personal_website = None
        self.review_mails_limit = 0
        self.notifications_frequency = 0
        db.session.commit()

    def can_upload_paper(self):
        count = PaperRevision.query.filter(PaperRevision.uploader_id
                                           == self.id,
                                           PaperRevision.publication_date
                                           == dt.datetime.utcnow().date()) \
            .count()
        if self.privileges_set >= UserTypeEnum.RESEARCHER_USER.value \
                and count < app.config['PAPER_L']:
            return True
        else:
            return False

    def can_comment(self):
        count = Comment.query.filter(Comment.creator == self.id,
                                     func.DATE(Comment.date)
                                     ==
                                     dt.datetime.utcnow().date()) \
            .count()
        if count < app.config['COMMENT_L']:
            return True
        else:
            return False

    def get_users_ids_whose_user_reviewed(self, days=10000):
        users_ids = set()
        date_after = dt.datetime.utcnow() - dt.timedelta(days=days)

        for review in self.rel_created_reviews:
            if (review.publication_datetime
                and review.publication_datetime >= date_after) \
                    or review.deadline_date >= date_after.date():

                for author in review.rel_related_paper_version.rel_creators:
                    users_ids.add(author.id)
        return users_ids

    def get_tags_to_user(self):
        return [association.tag for association in self.assoc_tags_to_user]

    # check if user can manage tag
    def can_edit_tagged_paper_reviewers(self, tag_id):
        if any(assoc.tag_id == tag_id for assoc in self.assoc_tags_to_user):
            return True
        else:
            return False

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': Markup.escape(self.first_name),
            'second_name': Markup.escape(self.second_name),
            'affiliation': Markup.escape(self.affiliation),
            'profile_url': url_for('user.profile_page', user_id=self.id),
            'profile_img_url': url_for('static', filename=f'res/profileImages/{self.id}.jpg') if self.has_photo else url_for('static',filename='res/profileImages/img.jpg'),
            'email': self.email
        }

#to introduce new badge it is nessesary to add on init deffinition of all badge objects in data_generator.py
#also you can add logic to add badges to certain entpoints or as triggers on db
class Badge(db.Model):
    __tablename__ = 'badges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(mc.B_NAME_L), unique=True, nullable=False)  # unique name for the trigger to recognize which badge to award
    description = db.Column(db.String(mc.B_DESCRIPTION_L), nullable=False)  # description of badge award requirements/conditions (for users), shown in the tooltip of the badge
    icon_unicode = db.Column(db.String(mc.B_ICON_UNICODE_L))  # character(s) of the badge icon/emoji (expected to be short, ideally one symbol or graphics)
    condition = db.Column(db.String(mc.B_CONDITION_L), nullable=False)  # for future usage: a string that can symbolically encode badge requirements, could be automatically parsed and executed to award a badge

    ref_user_badges = db.relationship('UserBadge', backref='badge', lazy=True)


class UserBadge(db.Model):
    __tablename__ = 'user_badges'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=dt.datetime.utcnow, nullable=False)


class PrivilegeSet(db.Model):
    __tablename__ = "privileges_sets"

    # primary keys
    # autoincrement=False becasue ID may represent a permission level
    id = db.Column(db.Integer(), primary_key=True, autoincrement=False)

    # columns
    name = db.Column(db.String(length=mc.PS_NAME_L),
                     nullable=False, unique=True)

    # relationships
    rel_users = db.relationship("User", back_populates="rel_privileges_set")
    rel_related_comments_ps = db.relationship("Comment", back_populates="rel_creator_role")

    def insert_types():
        for t in UserTypeEnum:
            if not PrivilegeSet.query.filter(PrivilegeSet.name == t.name) \
                    .first():
                privilege_set = PrivilegeSet(id=t.value, name=t.name)
                db.session.add(privilege_set)
        db.session.commit()

    def __repr__(self):
        return f'<PrivilegeSet {self.id} {self.name}>'


class Tag(db.Model):
    __tablename__ = "tags"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    # uppercase letters and digits (.isalnum())
    name = db.Column(db.String(length=mc.TAG_NAME_L),
                     nullable=False, unique=True)
    description = db.Column(
        db.String(length=mc.TAG_DESCRIPTION_L), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    red_flags_count = db.Column(db.Integer(), default=0, nullable=False)
    force_hide = db.Column(db.Boolean, nullable=False, default=False)
    force_show = db.Column(db.Boolean, nullable=False, default=False)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_related_paper_revisions = db.relationship("PaperRevision", secondary=association_tag_paper_version,
                                                  back_populates="rel_related_tags")

    assoc_users_with_this_tag = db.relationship(
        "AssociationTagUser", back_populates="rel_tag")

    rel_creator = db.relationship("User", back_populates="rel_created_tags")
    rel_red_flags_received = db.relationship(
        "RedFlagTag", back_populates="rel_to_tag")

    @validates('name')
    def convert_upper(self, key, value):
        return value.upper()

    # used in table with user's tag in user private profile
    def to_dict(self):
        creator = self.rel_creator
        return {
            'id': self.id,
            'name': Markup.escape(self.name),
            'description': Markup.escape(f'{self.description[:29]}...'),
            'deadline': self.deadline,
            'edit_url': url_for('tag.edit_tag_page', tag_id=self.id),
            'show_url': url_for('tag.tag_page', tag_name=Markup.escape(self.name)),
            'edit_members_url': url_for('tag.edit_tag_members_page', tag_id=self.id),
            'creator': Markup.escape(f'{creator.first_name} {creator.second_name}')
        }

    def get_users_with_this_tag(self):
        return [association.rel_user for association in self.assoc_users_with_this_tag]


class Paper(db.Model):
    __tablename__ = "papers"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # relationships
    rel_related_versions = db.relationship(
        "PaperRevision", back_populates="rel_parent_paper")

    def get_latest_revision(self):
        return max(self.rel_related_versions, key=lambda v: v.version)

    def to_dict(self):
        return {
            'id': self.id,
            'paper_title': Markup.escape(self.get_latest_revision().title),
            'publication_datetime': self.get_latest_revision().publication_date
        }

    def get_co_authors_ids(self, days=10000):
        ids = set()
        for revision in self.rel_related_versions:
            date_after = dt.datetime.utcnow() - dt.timedelta(days=days)
            if revision.publication_date >= date_after:
                for creator in revision.rel_creators:
                    ids.add(creator.id)
        return ids


class CalibrationPaper(db.Model):
    __tablename__ = "calibration_papers"

    # primary keys
    id = db.Column(db.Integer(), Sequence('seq_paper_id'), primary_key=True, autoincrement=True)

    # columns
    pdf_url = db.Column(db.String(mc.PV_PDF_URL_L), nullable=False)
    preprocessed_text = db.Column(db.Text(), nullable=True)
    description = db.Column(db.String(length=mc.CP_DESCRIPTION_L), nullable=True)

    # foreign keys
    author = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_author = db.relationship(
        "User", back_populates="rel_calibration_papers")


class UserPaperContribution(db.Model):
    __tablename__ = "user_paper_contribution"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    content = db.Column(db.String(length=mc.USER_CONTRIB_L), nullable=False)

    # foreign keys


class PaperRevision(db.Model):
    __tablename__ = "paper_revisions"

    # primary keys
    id = db.Column(db.Integer(), Sequence('seq_paper_id'), primary_key=True, autoincrement=True)

    # columns
    version = db.Column(db.Integer(), default=1, nullable=False)
    pdf_url = db.Column(db.String(mc.PV_PDF_URL_L), nullable=False)
    title = db.Column(db.String(length=mc.PV_TITLE_L), nullable=False)
    abstract = db.Column(db.String(length=mc.PV_ABSTRACT_L), nullable=False)
    publication_date = db.Column(db.DateTime)
    confidence_level = db.Column(db.SmallInteger(), default=0, nullable=False)
    red_flags_count = db.Column(db.Integer(), default=0, nullable=False)
    conflicts_of_interest = db.Column(db.String(length=mc.PV_CONFLICTS_OF_INTEREST_L), nullable=True)
    # is blank if no anonymous version exists
    anonymized_pdf_url = db.Column(db.String(mc.PV_PDF_URL_L), nullable=True)
    force_hide = db.Column(db.Boolean, nullable=False, default=False)
    force_show = db.Column(db.Boolean, nullable=False, default=False)
    preprocessed_text = db.Column(db.Text(), nullable=False)
    how_confident_sum = db.Column(db.Float(precision=2), nullable=False, default=0.0)   # blue number
    average_grade = db.Column(db.Float(precision=2), nullable=False, default=0.0)       # bold number
    average_novel = db.Column(db.Float(precision=2), nullable=False, default=0.0)       # 1-st number
    average_conclusion = db.Column(db.Float(precision=2), nullable=False, default=0.0)  # 2-nd number
    average_error = db.Column(db.Float(precision=2), nullable=False, default=0.0)       # 3-rd number
    average_organize = db.Column(db.Float(precision=2), nullable=False, default=0.0)    # 4-th number
    average_accept = db.Column(db.Float(precision=2), nullable=False, default=0.0)      # 5-th number

    # foreign keys
    parent_paper = db.Column(db.Integer, db.ForeignKey('papers.id'))
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_related_comments = db.relationship("Comment", secondary=association_comment_paper_version,
                                           back_populates="rel_related_paper_version")
    rel_related_tags = db.relationship("Tag", secondary=association_tag_paper_version,
                                       back_populates="rel_related_paper_revisions")
    rel_related_reviews = db.relationship(
        "Review", back_populates="rel_related_paper_version")
    rel_parent_paper = db.relationship(
        "Paper", back_populates="rel_related_versions")
    rel_related_review_requests = db.relationship(
        "ReviewRequest", back_populates="rel_related_paper_version")
    rel_creators = db.relationship("User", secondary=association_paper_version_user,
                                   back_populates="rel_created_paper_revisions")
    rel_related_licenses = db.relationship("License", secondary=association_paper_version_license,
                                           back_populates="rel_related_paper_revisions")
    rel_red_flags_received = db.relationship(
        "RedFlagPaperRevision", back_populates="rel_to_paper_revision")
    rel_changes = db.relationship(
        "RevisionChangesComponent", back_populates="rel_paper_revision")

    def to_dict(self):
        return {
            'id': self.id,
            'title': Markup.escape(self.title),
            'publication_date': self.publication_date,
            'version': self.version,
            'show_url': url_for('paper.article', id=self.parent_paper, version=self.version),
            # TODO: change new_verison
            'new_verison_url': url_for('paper.upload_new_revision', id=self.parent_paper),
            'reviews_count':\
            f'{len(self.get_published_reviews_list())}\
                 / {self.confidence_level}',
            'more_reviews_url': url_for('review.increase_needed_reviews', revision_id=self.id)
        }

    def get_published_reviews_list(self):
        return [review for review in self.rel_related_reviews if review.publication_datetime is not None]

    def get_missing_published_reviews_count(self):
        return max(0, self.confidence_level - len(self.get_published_reviews_list()))

    def get_active_accepted_review_requests_count(self):
        count = 0
        for review_request in self.rel_related_review_requests:
            if review_request.decision is True:
                count += 1
            elif review_request.decision is None and \
                    review_request.deadline_date \
                    >= dt.datetime.utcnow().date():
                count += 1
        return count

    def get_missing_reviewers_count(self):
        missing_count = self.get_missing_published_reviews_count()
        missing_count -= self.get_active_accepted_review_requests_count()
        return max(0, missing_count)

    def get_paper_co_authors_ids(self, days):
        return self.rel_parent_paper.get_co_authors_ids(days)

    def get_similar_revisions_ids(self):
        similar_revisions_ids = []

        similar_ids = se.get_similar_articles_to_articles(self.id)
        all_revisions_ids = [revision.id for revision in PaperRevision.query.all()]
        similar_revisions_ids = [id for id in similar_ids if id in all_revisions_ids]

        return similar_revisions_ids

    def get_similar_revisions(self):
        similar_revisions = []

        similar_revisions_ids = self.get_similar_revisions_ids()
        similar_revisions = PaperRevision.query.filter(PaperRevision.id.in_(similar_revisions_ids)).paginate().items

        return similar_revisions

    def get_similar_users_ids(self):
        similar_ids = []

        all_users = User.query.all()
        users_dict_id = {}
        for user in all_users:
            if user.id != 0:
                users_dict_id[user.id] = [revision.id for revision in user.rel_created_paper_revisions]

        similar_ids = se.get_similar_users_to_article(self.id, users_dict_id)

        return similar_ids

    def get_similar_users(self):
        similar_users = []

        similar_users_ids = self.get_similar_users_ids()
        similar_users = User.query.filter(User.id.in_(similar_users_ids)).all()

        return similar_users

    def get_previous_revisions(self):
        all_revisions = self.rel_parent_paper.rel_related_versions
        previous_revisions = []
        for revision in all_revisions:
            if revision.version < self.version:
                previous_revisions.append(revision)
        return previous_revisions


class Review(db.Model):
    __tablename__ = "reviews"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    # datetime of review's submission
    publication_datetime = db.Column(db.DateTime, nullable=True)
    # deadline of submitting review
    deadline_date = db.Column(db.Date, nullable=True)
    red_flags_count = db.Column(db.Integer(), nullable=False, default=0)
    edit_counter = db.Column(db.Integer(), nullable=False, default=0)
    is_anonymous = db.Column(db.Boolean, nullable=False, default=False)
    # Initially review should be hidden before publication
    is_hidden = db.Column(db.Boolean, nullable=False, default=True)
    force_hide = db.Column(db.Boolean, nullable=False, default=False)
    force_show = db.Column(db.Boolean, nullable=False, default=False)

    # evaluation criteria
    evaluation_novel = db.Column(
        db.Float(precision=2), nullable=False, default=0.0)
    evaluation_conclusion = db.Column(
        db.Float(precision=2), nullable=False, default=0.0)
    evaluation_error = db.Column(
        db.Float(precision=2), nullable=False, default=0.0)
    evaluation_organize = db.Column(
        db.Float(precision=2), nullable=False, default=0.0)
    evaluation_accept = db.Column(
        db.Boolean(), nullable=False, default=False)
    confidence = db.Column(db.Float(precision=2), nullable=False, default=0.0)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    related_paper_version = db.Column(
        db.Integer, db.ForeignKey('paper_revisions.id'))

    # relationships
    rel_comments_to_this_review = db.relationship("Comment", secondary=association_comment_review,
                                                  back_populates="rel_related_review_c")
    rel_creator = db.relationship("User", back_populates="rel_created_reviews")
    rel_related_paper_version = db.relationship(
        "PaperRevision", back_populates="rel_related_reviews")
    rel_red_flags_received = db.relationship(
        "RedFlagReview", back_populates="rel_to_review")
    rel_suggestions = db.relationship(
        "Suggestion", back_populates="rel_review")

    def get_paper_title(self):
        return db.session.query(PaperRevision.title).filter(
            PaperRevision.id == self.related_paper_version).scalar()

    def to_dict(self):
        paper_revision = self.rel_related_paper_version

        return {
            'id': self.id,
            'paper_title': Markup.escape(paper_revision.title),
            'paper_version': paper_revision.version,
            'publication_datetime': self.publication_datetime,
            'edit_url': url_for('review.review_edit_page', review_id=self.id),
            'is_visible': 'No' if self.is_hidden else 'Yes',
            'show_url': url_for('review.review_page', review_id=self.id)
        }

    def get_author_name(self):
        names = db.session.query(User.first_name, User.second_name).filter(
            User.id == self.rel_creator.id).first()
        print(names)
        return f'{names[0]} {names[1]}'

    def is_published(self):
        return self.publication_datetime != None

    # returns reviews connected to previous paper versions
    def get_previous_reviews(self):
        paper_revisions = self.rel_related_paper_version.rel_parent_paper.rel_related_versions
        previous_paper_revisions = [version for version in paper_revisions
                                    if version.version < self.rel_related_paper_version.version]
        previous_reviews = []
        for version in previous_paper_revisions:
            for review in version.rel_related_reviews:
                previous_reviews.append(review)

        return previous_reviews

    # returns reviews connected to previous paper versions written by self.creator
    def get_previous_creator_reviews(self):
        paper_revisions = self.rel_related_paper_version.rel_parent_paper.rel_related_versions
        previous_paper_revisions = [version for version in paper_revisions
                                    if version.version < self.rel_related_paper_version.version]
        previous_reviews = []
        for version in previous_paper_revisions:
            for review in version.rel_related_reviews:
                if review.creator == self.creator:
                    previous_reviews.append(review)

        return previous_reviews

    def can_be_edited(self):
        newest_revision_id = self.rel_related_paper_version \
            .rel_parent_paper.get_latest_revision().id
        if self.rel_related_paper_version.id == newest_revision_id:
            return True
        else:
            return False

    def can_show(self):
        if self.force_show and self.force_hide:
            raise ValueError("Both force_show and force_hide values can't be true")
        elif self.force_show:
            return True
        elif self.force_hide:
            return False
        elif self.is_hidden:
            return False
        else:
            return self.red_flags_count < app.config['RED_FLAGS_THRESHOLD']


class ReviewRequest(db.Model):
    __tablename__ = "review_requests"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    decision = db.Column(db.Boolean, nullable=True)
    creation_datetime = db.Column(db.DateTime)
    response_date = db.Column(db.Date)

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
    paper_version = db.Column(db.Integer, db.ForeignKey('paper_revisions.id'))

    # relationships
    rel_requested_user = db.relationship(
        "User", back_populates="rel_related_review_requests")
    rel_related_paper_version = db.relationship(
        "PaperRevision", back_populates="rel_related_review_requests")

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

    def can_request_after_decline(self):
        if self.decision is False:
            if self.reason_time is True:
                days = dt.timedelta(days=app.config['EXCLUDE_DECLINED_REQUEST_TIME_DAYS'])
                days_before = dt.datetime.utcnow().date() - days

                if self.response_date < days_before:
                    return True
                else:
                    return False
            return False
        return False

    def get_decision_string(self):
        if self.decision is True:
            return 'Accepted'
        elif self.decision is False:
            return 'Declined'
        else:
            return 'Pending'


class Comment(db.Model):
    __tablename__ = "comments"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    text = db.Column(db.String(length=mc.COMMENT_TEXT_L))
    votes_score = db.Column(db.Integer(), nullable=False, default=0)
    red_flags_count = db.Column(db.Integer(), nullable=False, default=0)
    level = db.Column(db.Integer(), nullable=False, default=0)
    date = db.Column(db.DateTime)
    force_hide = db.Column(db.Boolean, nullable=False, default=False)
    force_show = db.Column(db.Boolean, nullable=False, default=False)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator_role = db.Column(db.Integer, db.ForeignKey('privileges_sets.id'))
    comment_ref = db.Column(db.Integer, db.ForeignKey('comments.id'))

    # relationships
    rel_related_paper_version = db.relationship("PaperRevision", secondary=association_comment_paper_version,
                                                back_populates="rel_related_comments", uselist=False)
    rel_related_review_c = db.relationship("Review", secondary=association_comment_review,
                                           back_populates="rel_comments_to_this_review", uselist=False)
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
    rel_creator_role = db.relationship("PrivilegeSet", back_populates="rel_related_comments_ps")
    rel_forum_topic = db.relationship("ForumTopic", secondary=association_comment_forum_topic,
                                      back_populates="rel_comments", uselist=False)

    def to_dict(self):
        refers_to = ''
        show_url = url_for('main.home_page')
        paper_verison = self.rel_related_paper_version
        if paper_verison:
            refers_to = 'Paper'
            show_url = url_for('paper.article',
                               id=paper_verison.parent_paper,
                               version=paper_verison.version) \
                + f'#c{self.id}'

        review = self.rel_related_review_c
        if review:
            refers_to = 'Review'
            show_url = url_for('review.review_page', review_id=review.id) \
                + f'#c{self.id}'

        forum_topic = self.rel_forum_topic
        if forum_topic:
            refers_to = forum_topic.title
            show_url = url_for('forum.show_forum_topic', id=forum_topic.id)

        return {
            'id': self.id,
            'text': Markup.escape(f'{self.text[:50]}...'),
            'date': self.date,
            'votes_score': self.votes_score,
            'refers_to': refers_to,
            'show_url': show_url
        }


class MessageToStaff(db.Model):
    __tablename__ = "messages_to_staff"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    text = db.Column(db.String(length=mc.MTS_TEXT_L), nullable=False)
    date = db.Column(db.DateTime)
    replied = db.Column(db.Boolean, nullable=False, default=False)

    # foreign keys
    sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic = db.Column(db.Integer, db.ForeignKey('message_topics.id'))

    message_topics_enum = MessageTopicEnum

    # relationships
    rel_sender = db.relationship(
        "User", back_populates="rel_related_staff_messages")
    rel_topic = db.relationship(
        "MessageTopic", back_populates="rel_related_staff_messages")


class DeclinedReason(db.Model):
    __tablename__ = "declined_reasons"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    reason = db.Column(db.String(length=mc.DR_REASON_L), nullable=False)

    reasons = ('Conflict of interest', 'Lack of expertise',
               'Don’t have time', 'Paper matched incorrectly', 'Other')

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
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    topic = db.Column(db.String(length=mc.MT_TOPIC_L), nullable=False)

    # relationships
    rel_related_staff_messages = db.relationship(
        "MessageToStaff", back_populates="rel_topic")

    def insert_topics():
        for t in MessageTopicEnum:
            if not MessageTopic.query.filter(MessageTopic.topic == t.name).first():
                message_topic = MessageTopic(id=t.value, topic=t.name)
                db.session.add(message_topic)
        db.session.commit()

    def __repr__(self):
        return f'<MessageTopic {self.id} {self.topic}>'


class EmailType(db.Model):
    __tablename__ = 'email_types'

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    name = db.Column(db.String(length=mc.EM_TYPE_NAME_L),
                     nullable=False, unique=True)
    rel_email_logs = db.relationship("EmailLog")

    def insert_types():
        for t in EmailTypeEnum:
            if not EmailType.query.filter(EmailType.name == t.name).first():
                email_type = EmailType(id=t.value, name=t.name)
                db.session.add(email_type)
        db.session.commit()

    def __repr__(self):
        return f'<EmailType {self.id} {self.name}>'


class EmailLog(db.Model):
    __tablename__ = 'email_logs'

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, nullable=True)
    receiver_email = db.Column(
        db.String(length=mc.USER_EMAIL_L), nullable=False)
    date = db.Column(db.DateTime, nullable=True)

    # foreign keys
    email_type_id = db.Column(db.Integer, db.ForeignKey('email_types.id'))

    email_types_enum = EmailTypeEnum

    def __init__(self, sender_id, reciever_id,
                 reciever_email, date, email_type_id):
        self.sender_id = sender_id
        self.receiver_id = reciever_id
        self.receiver_email = reciever_email
        self.date = date
        self.email_type_id = email_type_id


class NotificationType(db.Model):
    __tablename__ = 'notification_types'

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    name = db.Column(db.String(length=mc.EM_TYPE_NAME_L),
                     nullable=False, unique=True)
    rel_email_logs = db.relationship("Notification",overlaps="rel_notifications")

    # relations
    rel_notifications = db.relationship(
        "Notification", back_populates="rel_notification_type", lazy='dynamic', overlaps="rel_email_logs")

    def insert_types():
        for t in NotificationTypeEnum:
            if not NotificationType.query.filter(NotificationType.name == t.name).first():
                notification_type = NotificationType(id=t.value, name=t.name)
                db.session.add(notification_type)
        db.session.commit()

    def __repr__(self):
        return f'<NotificationType {self.id} {self.name}>'


class Notification(db.Model):
    __tablename__ = 'notifications'

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    datetime = db.Column(db.DateTime, nullable=False)
    title = db.Column(
        db.String(length=mc.NOTIFICATION_TITLE_L), nullable=False)
    text = db.Column(db.String(length=mc.NOTIFICATION_TEXT_L), nullable=False)
    action_url = db.Column(
        db.String(length=mc.NOTIFICATION_ACTION_URL_L), nullable=True)
    was_seen = db.Column(db.Boolean, nullable=False, default=False)

    # foreign keys
    notification_type = db.Column(
        db.Integer, db.ForeignKey('notification_types.id'))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_notification_type = db.relationship(
        "NotificationType", back_populates="rel_notifications", overlaps="rel_email_logs")
    rel_user = db.relationship("User", back_populates="rel_notifications")

    notification_types_enum = NotificationTypeEnum

    # returns notification title (string) based on notification type
    def prepare_title(notification_type):
        if isinstance(notification_type, str):
            type_string = notification_type
        elif isinstance(notification_type, NotificationType):
            type_string = str(notification_type.name)
        elif isinstance(notification_type, int):
            type_string = NotificationType.query.filter(
                NotificationType.id == notification_type).first().name

        return type_string.replace('_', ' ').lower().capitalize()


class Suggestion(db.Model):
    __tablename__ = "suggestions"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    suggestion = db.Column(db.String(length=mc.S_SUGGESTION_L), nullable=False)
    location = db.Column(db.String(length=mc.S_LOCATION_L))

    # foreign keys
    review = db.Column(db.Integer, db.ForeignKey(
        'reviews.id'))

    # relationships
    rel_review = db.relationship("Review", back_populates="rel_suggestions")
    rel_revision_change_component = db.relationship("RevisionChangesComponent",
                                                    back_populates='rel_review_suggestion', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'suggestion': Markup.escape(self.suggestion),
            'location': Markup.escape(self.location)
        }

    @validates('suggestion')
    def set_suggestion(self, key, value):
        if len(value) > mc.S_SUGGESTION_L:
            return value[:mc.S_SUGGESTION_L]
        else:
            return value

    @validates('location')
    def set_location(self, key, value):
        if value and len(value) > mc.S_LOCATION_L:
            return value[:mc.S_LOCATION_L]
        else:
            return value


class License(db.Model):
    __tablename__ = "licenses"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    license = db.Column(db.String(length=mc.L_LICENSE_L), nullable=False)

    # relationships
    rel_related_paper_revisions = db.relationship("PaperRevision", secondary=association_paper_version_license,
                                                  back_populates="rel_related_licenses")

    @classmethod
    def insert_licenses(cls):
        for license_name, license_id in LICENSE_DICT.items():
            if not License.query.filter(License.license == license_name).first():
                license_to_add = License(id=license_id, license=license_name)
                db.session.add(license_to_add)
        db.session.commit()


class RevisionChangesComponent(db.Model):
    __tablename__ = "revision_changes_components"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # columns
    change_description = db.Column(
        db.String(length=mc.RCC_CHANGE_DESCRIPTION_L), nullable=False)
    location = db.Column(db.String(length=mc.S_LOCATION_L))

    # foreign keys
    paper_revision = db.Column(db.Integer, db.ForeignKey(
        'paper_revisions.id'))
    review_suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestions.id'))

    # relationships
    rel_paper_revision = db.relationship(
        "PaperRevision", back_populates="rel_changes")

    rel_review_suggestion = db.relationship("Suggestion", back_populates="rel_revision_change_component", uselist=False)


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
    rel_creator = db.relationship(
        "User", back_populates="rel_comment_votes_created")
    rel_to_comment = db.relationship(
        "Comment", back_populates="rel_comment_votes_received")


class RedFlagComment(db.Model):
    __tablename__ = "red_flags_comment"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_comment = db.Column(db.Integer, db.ForeignKey('comments.id'))

    # relationships
    rel_creator = db.relationship(
        "User", back_populates="rel_comment_red_flags", foreign_keys=[creator])
    rel_to_comment = db.relationship(
        "Comment", back_populates="rel_red_flags_received", foreign_keys=[to_comment])


class RedFlagPaperRevision(db.Model):
    __tablename__ = "red_flags_paper_revision"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_paper_revision = db.Column(
        db.Integer, db.ForeignKey('paper_revisions.id'))

    # relationships
    rel_creator = db.relationship(
        "User", back_populates="rel_paper_version_red_flags")
    rel_to_paper_revision = db.relationship(
        "PaperRevision", back_populates="rel_red_flags_received")


class RedFlagReview(db.Model):
    __tablename__ = "red_flags_review"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_review = db.Column(db.Integer, db.ForeignKey('reviews.id'))

    # relationships
    rel_creator = db.relationship(
        "User", back_populates="rel_review_red_flags")
    rel_to_review = db.relationship(
        "Review", back_populates="rel_red_flags_received")


class RedFlagTag(db.Model):
    __tablename__ = "red_flags_tag"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_tag = db.Column(db.Integer, db.ForeignKey('tags.id'))

    # relationships
    rel_creator = db.relationship("User", back_populates="rel_tag_red_flags")
    rel_to_tag = db.relationship(
        "Tag", back_populates="rel_red_flags_received")


class RedFlagUser(db.Model):
    __tablename__ = "red_flags_user"

    # primary keys
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    # foreign keys
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships
    rel_creator = db.relationship(
        "User", back_populates="rel_user_red_flags", foreign_keys=[creator])
    rel_to_user = db.relationship(
        "User", back_populates="rel_red_flags_received", foreign_keys=[to_user])


class EndorsementRequestLog(db.Model):
    __tablename__ = "endorsement_request_logs"

    # columns
    decision = db.Column(db.Boolean(), default=False, nullable=False)
    date = db.Column(db.Date(), nullable=False)
    considered = db.Column(db.Boolean(), default=False, nullable=False)

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    endorser_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def get_endorsement_request_count(user_id, days):
        date_after = dt.datetime.utcnow().date() - dt.timedelta(days=days)
        count = EndorsementRequestLog.query.filter(EndorsementRequestLog.user_id == user_id,
                                                   func.DATE(
                                                       EndorsementRequestLog.date) > date_after,
                                                   EndorsementRequestLog.decision == True).count()
        return count


class ForumTopic(db.Model):
    __tablename__ = "forum_topics"

    # primary keys
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # columns
    title = db.Column(db.String(length=200), nullable=False)
    content = db.Column(db.String(length=1000), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime)

    # relationships
    rel_comments = db.relationship("Comment", secondary=association_comment_forum_topic,
                                   back_populates="rel_forum_topic")
    def to_dict(self):

        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'date_created': self.date_created,
            'show_url': url_for('forum.show_forum_topic', id=self.id)
        }


# db functions
db_fun_update_comment_score = DDL(q_update_comment_score)
db_fun_update_user_reputation = DDL(q_update_user_reputation)
db_fun_update_user_red_flags_count = DDL(q_update_user_red_flags_count)
db_fun_update_tag_red_flags_count = DDL(q_update_tag_red_flags_count)
db_fun_update_review_red_flags_count = DDL(q_update_review_red_flags_count)
db_fun_update_revision_red_flags_count = DDL(q_update_revision_red_flags_count)
db_fun_update_comment_red_flags_count = DDL(q_update_comment_red_flags_count)
db_fun_update_revision_averages = DDL(q_update_revision_averages)
db_fun_update_badge_first_article = DDL(b_first_article_award_function)
db_fun_update_badge_first_comment = DDL(b_first_comment_award_function)

# db triggers
db_trig_update_comment_score = DDL(qt_update_comment_score)
db_trig_update_user_reputation = DDL(qt_update_user_reputation)
db_trig_update_user_red_flags_count = DDL(qt_update_user_red_flags_count)
db_trig_update_tag_red_flags_count = DDL(qt_update_tag_red_flags_count)
db_trig_update_review_red_flags_count = DDL(qt_update_review_red_flags_count)
db_trig_update_revision_red_flags_count = DDL(qt_update_revision_red_flags_count)
db_trig_update_comment_red_flags_count = DDL(qt_update_comment_red_flags_count)
db_trig_update_revision_averages = DDL(qt_update_revision_averages)
db_trig_update_badge_first_article = DDL(b_first_article_award_trigger)
db_trig_update_badge_first_comment = DDL(b_first_comment_award_trigger)

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

event.listen(
    Comment.__table__,
    'after_create',
    db_fun_update_user_reputation.execute_if(dialect='postgresql')
)

event.listen(
    Comment.__table__,
    'after_create',
    db_trig_update_user_reputation.execute_if(dialect='postgresql')
)

event.listen(
    RedFlagUser.__table__,
    'after_create',
    db_fun_update_user_red_flags_count.execute_if(dialect='postgresql')
)

event.listen(
    RedFlagUser.__table__,
    'after_create',
    db_trig_update_user_red_flags_count.execute_if(dialect='postgresql')
)

event.listen(
    RedFlagTag.__table__,
    'after_create',
    db_fun_update_tag_red_flags_count.execute_if(dialect='postgresql')
)

event.listen(
    RedFlagTag.__table__,
    'after_create',
    db_trig_update_tag_red_flags_count.execute_if(dialect='postgresql')
)

event.listen(
    RedFlagReview.__table__,
    'after_create',
    db_fun_update_review_red_flags_count.execute_if(dialect='postgresql')
)

event.listen(
    RedFlagReview.__table__,
    'after_create',
    db_trig_update_review_red_flags_count.execute_if(dialect='postgresql')
)

event.listen(
    RedFlagPaperRevision.__table__,
    'after_create',
    db_fun_update_revision_red_flags_count.execute_if(dialect='postgresql')
)

event.listen(
    RedFlagPaperRevision.__table__,
    'after_create',
    db_trig_update_revision_red_flags_count.execute_if(dialect='postgresql')
)

event.listen(
    RedFlagComment.__table__,
    'after_create',
    db_fun_update_comment_red_flags_count.execute_if(dialect='postgresql')
)

event.listen(
    RedFlagComment.__table__,
    'after_create',
    db_trig_update_comment_red_flags_count.execute_if(dialect='postgresql')
)

event.listen(
    Review.__table__,
    'after_create',
    db_fun_update_revision_averages.execute_if(dialect='postgresql')
)

event.listen(
    Review.__table__,
    'after_create',
    db_trig_update_revision_averages.execute_if(dialect='postgresql')
)

event.listen(
    PaperRevision.__table__,
    'after_create',
    db_fun_update_badge_first_article.execute_if(dialect='postgresql')
)

event.listen(
    PaperRevision.__table__,
    'after_create',
    db_trig_update_badge_first_article.execute_if(dialect='postgresql')
)

event.listen(
    Comment.__table__,
    'after_create',
    db_fun_update_badge_first_comment.execute_if(dialect='postgresql')
)

event.listen(
    Comment.__table__,
    'after_create',
    db_trig_update_badge_first_comment.execute_if(dialect='postgresql')
)
