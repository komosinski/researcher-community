import math
import os
import random
import time
import requests

from flask import url_for
from werkzeug.utils import secure_filename

from config.config import Config
from data_generator.consts import name_surname_list, tags
from open_science import db
from open_science.enums import UserTypeEnum
from open_science.models import PrivilegeSet, DeclinedReason, MessageTopic, EmailType, NotificationType, License, User, \
    PaperRevision, Comment, Paper, Review, Tag, ReviewRequest, VoteComment, MessageToStaff, Notification, Suggestion, \
    CalibrationPaper, RevisionChangesComponent, RedFlagComment, RedFlagPaperRevision, RedFlagReview, RedFlagTag, \
    RedFlagUser, AssociationTagUser
import datetime as dt
import text_processing.similarity_matrix as sm

from text_processing.plot import create_save_users_plot, create_save_users_plot_3d
from text_processing.prepocess_text import get_text, preprocess_text
from config import models_config as mc

class DataGenerator:
    # default counts of objects to be created in database
    # they can be overwrite through objects_count_dict values given in constructor
    default_users_count = 100
    default_papers_count = 200
    default_revisions_count = 600
    default_reviews_count = 1800
    default_tags_count = 400
    default_comments_count = 500
    default_review_requests_count = 3000
    default_votes_count = 3000
    default_staff_messages_count = 10
    default_notifications_count = 3000
    default_suggestions_count = 5000
    default_calibration_papers_count = 200
    default_changes_components_count = 5000
    default_comments_flags_count = 100
    default_revisions_flags_count = 10
    default_reviews_flags_count = 10
    default_tags_flags_count = 10
    default_users_flags_count = 5

    # const strings to pass to the objects_count_dict
    str_users_count = 'USERS_COUNT'
    str_papers_count = 'PAPERS_COUNT'
    str_revisions_count = 'REVISIONS_COUNT'
    str_reviews_count = 'REVIEWS_COUNT'
    str_tags_count = 'TAGS_COUNT'
    str_comments_count = 'COMMENTS_COUNT'
    str_review_requests_count = 'REVIEW_REQUESTS_COUNT'
    str_votes_count = 'VOTES_COUNT'
    str_staff_messages_count = 'STAFF_MESSAGES_COUNT'
    str_notifications_count = 'NOTIFICATIONS_COUNT'
    str_suggestions_count = 'SUGGESTIONS_COUNT'
    str_calibration_papers_count = 'CALIBRATION_PAPERS_COUNT'
    str_changes_components_count = 'CHANGES_COMPONENTS_COUNT'
    str_comments_flags_count = 'COMMENTS_FLAGS_COUNT'
    str_revisions_flags_count = 'REVISIONS_FLAGS_COUNT'
    str_reviews_flags_count = 'REVIEWS_FLAGS_COUNT'
    str_tags_flags_count = 'TAGS_FLAGS_COUNT'
    str_users_flags_count = 'USERS_FLAGS_COUNT'

    start_datetime = dt.datetime(2020, 1, 1, 1, 1, 1, 1)

    def __init__(self, app, objects_count_overwrite_dict=None, seed=None):
        if objects_count_overwrite_dict is None:
            objects_count_overwrite_dict = {}

        self.use_random_words_for_revisions = False
        
        self.app = app
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)

        default_objects_count_dict = {
            self.str_users_count: self.default_users_count,
            self.str_papers_count: self.default_papers_count,
            self.str_revisions_count: self.default_revisions_count,
            self.str_reviews_count: self.default_reviews_count,
            self.str_tags_count: self.default_tags_count,
            self.str_comments_count: self.default_comments_count,
            self.str_review_requests_count: self.default_review_requests_count,
            self.str_votes_count: self.default_votes_count,
            self.str_staff_messages_count: self.default_staff_messages_count,
            self.str_notifications_count: self.default_notifications_count,
            self.str_suggestions_count: self.default_suggestions_count,
            self.str_calibration_papers_count: self.default_calibration_papers_count,
            self.str_changes_components_count: self.default_changes_components_count,
            self.str_comments_flags_count: self.default_comments_flags_count,
            self.str_revisions_flags_count: self.default_revisions_flags_count,
            self.str_reviews_flags_count: self.default_reviews_flags_count,
            self.str_tags_flags_count: self.default_tags_flags_count,
            self.str_users_flags_count: self.default_users_flags_count,
        }

        self.objects_count_dict = default_objects_count_dict.copy()

        for key, value in objects_count_overwrite_dict.items():
            if key in default_objects_count_dict.keys():
                self.objects_count_dict[key] = value

        self.counts_validation()

    def counts_validation(self):
        papers_count = self.objects_count_dict[self.str_papers_count]
        revisions_count = self.objects_count_dict[self.str_revisions_count]
        if revisions_count < papers_count:
            raise "There can't be more papers than revisions"

    def create_text_processing_data(self):
        with self.app.app_context():
            try:
                print('creating similarity matrix...')
                dictionary = sm.create_dictionary()
                sm.save_dictionary(dictionary)
                tfidf_matrix = sm.create_tfidf_matrix()
                sm.save_tfidf_matrix(tfidf_matrix)

                start = time.time()
                similarities_matrix = sm.create_similarities_matrix()
                end = time.time()
                print(f"creating similarities matrix took {end - start} seconds")

                sm.save_similarities_matrix(similarities_matrix)
                print('creating 2D plot...')
                create_save_users_plot()
                print('2D plot has been created')
                print('creating 3D plot...')
                create_save_users_plot_3d()
                print('3D plot has been created')
                return True
            except Exception as e:
                print(e)
                return False
            
    def generate_data(self):
        with self.app.app_context():
            if PaperRevision.query.all():
                return False
            else:
                self.create_essential_data()
                self.generate_users()
                self.generate_papers()
                self.generate_paper_revisions()
                self.generate_reviews()
                self.generate_tags()
                self.generate_comments()
                self.generate_review_requests()
                self.generate_votes()
                self.generate_messages_to_staff()
                self.generate_notifications()
                self.generate_suggestions()
                self.generate_calibration_papers()
                self.generate_revision_changes_components()
                self.generate_comments_red_flags()
                self.generate_paper_revisions_red_flags()
                self.generate_reviews_red_flags()
                self.generate_tags_red_flags()
                self.generate_users_red_flags()

                print('committing ...')
                db.session.commit()

    def create_essential_data(self):
        PrivilegeSet.insert_types()
        DeclinedReason.insert_reasons()
        MessageTopic.insert_topics()
        EmailType.insert_types()
        NotificationType.insert_types()
        License.insert_licenses()

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
            user_0.rel_privileges_set = PrivilegeSet.query.filter(
                PrivilegeSet.id == UserTypeEnum.STANDARD_USER.value).first()
            user_0.id = 0
            db.session.add(user_0)

        db.session.commit()
        print("The essential data has been created")

        return True

    def generate_users(self):
        users_count = self.objects_count_dict[self.str_users_count]

        for user_number in range(users_count):
            name_surname = random.choice(name_surname_list)
            first_name = name_surname.split()[0]
            second_name = name_surname.split()[1]
            email = f"{first_name}.{second_name}{user_number}@email.com"
            review_mails_limit = random.choice(range(5))
            notifications_frequency = random.choice([0, 1, 3, 7, 15, 30])
            weight = round(random.uniform(1, 5), 2)
            privileges_set_ids = [privileges_set.id for privileges_set in PrivilegeSet.query.all()]
            privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == random.choice(privileges_set_ids)).first()

            registered_on = self.start_datetime + dt.timedelta(days=user_number)
            confirmed_on = registered_on + dt.timedelta(days=1)
            last_seen = registered_on + dt.timedelta(days=335)

            user = User(
                first_name=first_name,
                second_name=second_name,
                email=email,
                plain_text_password="QWerty12#$%",
                confirmed=True,
                confirmed_on=confirmed_on,
                affiliation="university",
                orcid="0000000218250091",
                google_scholar="https://scholar.google.com/profilX",
                about_me="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut mauris dui, posuere in purus vitae, "
                         "tristique elementum mi. Quisque maximus nunc ante, et interdum purus condimentum tincidunt. Ut eu "
                         "magna eget enim viverra maximus. Nulla non rhoncus odio, id ullamcorper lectus. Proin quis ligula "
                         "pretium, hendrerit erat non, rutrum enim. Pellentesque aliquam suscipit magna, vel ultrices ligula "
                         "feugiat vitae. Sed lacinia mauris vitae turpis hendrerit, vel luctus arcu sagittis. Pellentesque "
                         "habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus sit amet "
                         "libero eleifend, consequat justo nec, hendrerit risus. Vestibulum condimentum nec ex vel "
                         "consectetur. Duis in ipsum sit amet tellus rhoncus gravida sed ut magna. Suspendisse facilisis "
                         "vulputate pellentesque.",
                personal_website="https://personalwebsite.com",
                review_mails_limit=review_mails_limit,
                notifications_frequency=notifications_frequency,
                last_seen=last_seen,
                weight=weight,
                registered_on=registered_on
            )
            user.rel_privileges_set = privileges_set
            db.session.add(user)
        print("Users created")

    def generate_papers(self):
        papers_count = self.objects_count_dict[self.str_papers_count]

        for _ in range(papers_count):
            paper = Paper()
            db.session.add(paper)
        print("Papers created")

    def generate_paper_revisions(self):
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(word_site)
        WORDS = response.content.splitlines()

        versions_count_per_paper_list = self.get_versions_count_per_paper_list()
        revision_number = 1
        for paper_number, versions_count in enumerate(versions_count_per_paper_list):
            paper_id = paper_number + 1
            parent_paper = Paper.query.filter(Paper.id == paper_id).first()
            for version in range(1, versions_count + 1):
                revision = PaperRevision(
                    version=version,
                    pdf_url=os.path.join(Config.TEST_PDFS_DIR_PATH, secure_filename(f"{paper_id}.pdf")),
                    title="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer "
                          "commodo scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget",
                    abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus."
                             "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar"
                             "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis"
                             "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent"
                             "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum,"
                             "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel"
                             "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel"
                             "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet. "
                             "Suspendisse auctor id orci quis placerat.",
                    preprocessed_text=preprocess_text(" ".join([w.decode("utf-8") for w in random.choices(WORDS, k=1000)])),
                    confidence_level=3
                )

                if self.use_random_words_for_revisions:
                    revision.preprocessed_text = preprocess_text(" ".join([w.decode("utf-8") for w in random.choices(WORDS, k=1000)]))
                else:
                    revision.preprocessed_text = get_text(os.path.join(Config.PDFS_DIR_PATH, secure_filename(f"{paper_id}.pdf")))

                revision.rel_related_licenses = random.sample(License.query.all(), random.choice([1, 2, 3]))
                revision.rel_parent_paper = parent_paper
                revision.rel_creators = random.sample(User.query.filter(User.id != 0).all(),
                                                      random.choice([1, 2, 3, 4, 5]))
                publication_date = max([user.confirmed_on for user in revision.rel_creators])
                revision.publication_date = publication_date
                db.session.add(revision)

                revision_number += 1
        print("Paper revisions created")

    def get_versions_count_per_paper_list(self):
        revisions_count = self.objects_count_dict[self.str_revisions_count]
        papers_count = self.objects_count_dict[self.str_papers_count]

        revisions_per_paper_counts = []
        unasigned_revisions_count = revisions_count
        for paper_number in range(papers_count):
            is_last_paper = paper_number == papers_count - 1
            if is_last_paper:
                revisions_per_paper_counts.append(unasigned_revisions_count)
            else:
                unasigned_papers_count = papers_count - paper_number
                avg_rev_per_paper_unasigned = unasigned_revisions_count / unasigned_papers_count
                max_count = math.trunc(avg_rev_per_paper_unasigned * 2)
                revisions_per_this_paper_count = random.choice(range(1, max_count))
                revisions_per_paper_counts.append(revisions_per_this_paper_count)
                unasigned_revisions_count -= revisions_per_this_paper_count

        return revisions_per_paper_counts

    def generate_reviews(self):
        reviews_count = self.objects_count_dict[self.str_reviews_count]

        for _ in range(reviews_count):
            evaluation_novel = round(random.uniform(0, 1), 2)
            evaluation_conclusion = round(random.uniform(0, 1), 2)
            evaluation_error = round(random.uniform(0, 1), 2)
            evaluation_organize = round(random.uniform(0, 1), 2)
            confidence = round(random.uniform(0, 1), 2)

            review = Review(
                is_hidden=False,
                evaluation_novel=evaluation_novel,
                evaluation_conclusion=evaluation_conclusion,
                evaluation_error=evaluation_error,
                evaluation_organize=evaluation_organize,
                evaluation_accept=True,
                confidence=confidence,
            )
            review.rel_creator = random.choice(User.query.filter(User.id != 0).all())
            review.rel_related_paper_version = random.choice(PaperRevision.query.all())
            review.publication_datetime = max(review.rel_creator.confirmed_on,
                                              review.rel_related_paper_version.publication_date) \
                                          + dt.timedelta(days=random.choice([1, 2, 3])),
            db.session.add(review)
        print("Reviews created")

    def generate_tags(self):
        tags_count = self.objects_count_dict[self.str_tags_count]

        for tag_number in range(tags_count):
            name = f"{random.choice(tags)}{tag_number}"

            tag = Tag(
                name=name,
                description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
            )
            tag.creation_date = self.start_datetime  # tmp - overwritten later in this method
            tag.rel_creator = random.choice(User.query.filter(User.id != 0).all())
            tag.rel_related_paper_revisions = random.sample(PaperRevision.query.all(), random.choice([1, 2, 3, 4, 5]))

            # create association with tag's creator
            association_tag_user = AssociationTagUser(can_appoint=True, can_edit=True)
            association_tag_user.appointer_id = tag.creator
            association_tag_user.rel_user = tag.rel_creator
            association_tag_user.rel_tag = tag
      
            # create association with other users
            users_to_this_tag = random.sample(User.query.filter(User.id != 0, User.id!=tag.rel_creator.id).all(),
                                                        random.choice([1, 2, 3, 4, 5]))
            for user in users_to_this_tag:
                association_tag_user = AssociationTagUser(can_appoint=False, can_edit=False)
                association_tag_user.rel_user = user
                association_tag_user.rel_tag = tag
                association_tag_user.appointer_id = tag.creator
              
            tag.creation_date = max(
                tag.rel_creator.confirmed_on,
                max([revision.publication_date for revision in tag.rel_related_paper_revisions]),
                max([association.rel_user.confirmed_on for association in tag.assoc_users_with_this_tag])
            ) + dt.timedelta(days=random.choice([1, 2, 3]))
            tag.deadline = tag.creation_date + dt.timedelta(days=1095)
            db.session.add(tag)
        print("Tags created")

    def generate_comments(self):
        comments_count = self.objects_count_dict[self.str_comments_count]

        for comment_number in range(comments_count):
            comment = Comment(
                text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan. "
                     "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                     "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                     "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante  "
                     "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida  "
                     "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare.  "
                     "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero , "
                     "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante."
            )
            comment.rel_creator = random.choice(User.query.filter(User.id != 0).all())
            comment.rel_creator_role = comment.rel_creator.rel_privileges_set
            comment_to = random.choice([0, 1, 2]) if comment_number > 1 else random.choice([1, 2])
            if comment_to == 0:
                # weird because of uselist=False in model
                related_comment = random.sample(Comment.query.filter(
                    Comment.id != len(Comment.query.all()) - 1).all(), 1)[0]
                related_comment.rel_comments_to_this_comment.append(comment)
                if related_comment.date:
                    comment.date = max(
                        comment.rel_creator.confirmed_on,
                        related_comment.date
                    ) + dt.timedelta(days=random.choice([1, 2, 3]))
                else:
                    comment.date = comment.rel_creator.confirmed_on + dt.timedelta(days=random.choice([1, 2, 3]))
                comment.level = related_comment.level + 1
            elif comment_to == 1:
                related_review = random.choice(Review.query.all())
                related_review.rel_comments_to_this_review.append(comment)
                comment.date = max(
                    comment.rel_creator.confirmed_on,
                    related_review.publication_datetime[0]  # weird because of uselist=False in model
                ) + dt.timedelta(days=random.choice([1, 2, 3]))
                comment.level = 0
            else:
                comment.rel_related_paper_version = random.choice(PaperRevision.query.all())
                comment.date = max(
                    comment.rel_creator.confirmed_on,
                    comment.rel_related_paper_version.publication_date
                ) + dt.timedelta(days=random.choice([1, 2, 3]))
                comment.level = 0
            db.session.add(comment)
        print("Comments created")

    def generate_review_requests(self):
        review_requests_count = self.objects_count_dict[self.str_review_requests_count]

        for _ in range(review_requests_count):
            decision = random.choice([True, False])

            review_request = ReviewRequest(
                decision=decision,
            )
            review_request.rel_requested_user = random.choice(User.query.filter(User.id != 0).all())
            review_request.rel_related_paper_version = random.choice(PaperRevision.query.all())
            review_request.creation_datetime = review_request.rel_related_paper_version.publication_date \
                                               + dt.timedelta(days=random.choice([1, 2, 3]))
            review_request.response_date = review_request.creation_datetime \
                                           + dt.timedelta(days=random.choice([1, 2, 3]))
            review_request.deadline_date = review_request.response_date + dt.timedelta(days=30)
            db.session.add(review_request)
        print("Review requests created")

    def generate_votes(self):
        votes_count = self.objects_count_dict[self.str_votes_count]

        for _ in range(votes_count):
            is_up = random.choice([True, False])
            vote = VoteComment(
                is_up=is_up
            )
            vote.rel_creator = random.choice(User.query.filter(User.id != 0).all())
            vote.rel_to_comment = random.choice(Comment.query.all())
            db.session.add(vote)
        print("Comment votes created")

    def generate_messages_to_staff(self):
        staff_messages_count = self.objects_count_dict[self.str_staff_messages_count]

        for message_number in range(staff_messages_count):
            text = f"message{message_number}"
            replied = random.choice([True, False])

            staff_message = MessageToStaff(
                text=text,
                replied=replied
            )
            staff_message.rel_sender = random.choice(User.query.filter(User.id != 0).all())
            staff_message.rel_topic = random.choice(MessageTopic.query.all())
            staff_message.date = staff_message.rel_sender.confirmed_on + dt.timedelta(days=random.choice([1, 2, 3]))
            db.session.add(staff_message)
        print("Messages to staff created")

    def generate_notifications(self):
        notifications_count = self.objects_count_dict[self.str_notifications_count]

        for notification_number in range(notifications_count):
            notification_type = random.choice(NotificationType.query.all())
            title = Notification.prepare_title(notification_type)
            text = f"notification{notification_number}"
            request = random.choice(ReviewRequest.query.all())
            action_url = url_for('review.review_request_page', request_id=request.id)
            datetime = request.creation_datetime

            notification = Notification(
                datetime=datetime,
                title=title,
                text=text,
                action_url=action_url
            )
            notification.rel_notification_type = notification_type
            notification.rel_user = random.choice(User.query.filter(User.id != 0).all())
            db.session.add(notification)
        print("Notifications created")

    def generate_suggestions(self):
        suggestions_count = self.objects_count_dict[self.str_suggestions_count]

        for suggestion_number in range(suggestions_count):
            suggestion = Suggestion(
                suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus  a "
                           "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed  a, "
                           "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere  "
                           "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus.  diam "
                           "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt.  "
                           "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                           "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt.  "
                           "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                           "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus . "
                           "Etiam commodo tortor sit amet vulputate bibendum.",
                location="Page1"
            )
            suggestion.rel_review = random.choice(Review.query.all())
            db.session.add(suggestion)
        print("Suggestions created")

    def generate_calibration_papers(self):
        calibration_papers_count = self.objects_count_dict[self.str_calibration_papers_count]

        for calibration_paper_number in range(calibration_papers_count):
            pdf_url = os.path.join(Config.TEST_PDFS_DIR_PATH, secure_filename(f"{calibration_paper_number + 1}.pdf"))
            preprocessed_text = get_text(os.path.join(Config.PDFS_DIR_PATH,
                                                      secure_filename(f"{calibration_paper_number + 1}.pdf")))

            calibration_paper = CalibrationPaper(
                pdf_url=pdf_url,
                preprocessed_text=preprocessed_text,
                description=preprocessed_text[:mc.CP_DESCRIPTION_L]
            )
            calibration_paper.rel_author = random.choice(User.query.filter(User.id != 0).all())
            db.session.add(calibration_paper)
        print("Calibration papers created")

    def generate_revision_changes_components(self):
        revision_changes_components_count = self.objects_count_dict[self.str_changes_components_count]

        for _ in range(revision_changes_components_count):
            revision_changes_component = RevisionChangesComponent(
                change_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum  dapibus "
                                   "augue a suscipit. Proin ullamcorper nunc in feugiat porttitor.  risus dolor, "
                                   "luctus sed nulla a, hendrerit blandit tortor. Ut consectetur  diam in egestas. "
                                   "Vestibulum posuere imperdiet tincidunt. Pellentesque  nisi at velit dapibus, "
                                   "vel blandit mi maximus. Cras diam sem, ultricies et quam vel,   dolor. Nam "
                                   "eu nunc nec orci euismod tincidunt. Nulla nisl libero, aliuet ut ante sed, "
                                   "auctor aliquet mauris. Donec vel dapibus sem. Morbi eget interdum felis, eu  "
                                   "mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam ante neque, "
                                   "consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut  "
                                   "sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget,  nunc. "
                                   "Etiam commodo tortor sit amet vulputate bibendum.",
                location="Page1"
            )
            revision_changes_component.rel_paper_revision = random.choice(PaperRevision.query.all())
            db.session.add(revision_changes_component)
        print("Revision changes components created")

    def generate_comments_red_flags(self):
        comments_count = self.objects_count_dict[self.str_comments_flags_count]

        for _ in range(comments_count):
            red_flag_comment = RedFlagComment()
            red_flag_comment.rel_creator = random.choice(User.query.filter(User.id != 0).all())
            red_flag_comment.rel_to_comment = random.choice(Comment.query.all())
            db.session.add(red_flag_comment)
        print("Comments red flags created")

    def generate_paper_revisions_red_flags(self):
        revisions_count = self.objects_count_dict[self.str_revisions_flags_count]

        for _ in range(revisions_count):
            red_flag_revision = RedFlagPaperRevision()
            red_flag_revision.rel_creator = random.choice(User.query.filter(User.id != 0).all())
            red_flag_revision.rel_to_paper_revision = random.choice(PaperRevision.query.all())
            db.session.add(red_flag_revision)
        print("Revisions red flags created")

    def generate_reviews_red_flags(self):
        reviews_count = self.objects_count_dict[self.str_reviews_flags_count]

        for _ in range(reviews_count):
            red_flag_review = RedFlagReview()
            red_flag_review.rel_creator = random.choice(User.query.filter(User.id != 0).all())
            red_flag_review.rel_to_review = random.choice(Review.query.all())
            db.session.add(red_flag_review)
        print("Reviews red flags created")

    def generate_tags_red_flags(self):
        tags_count = self.objects_count_dict[self.str_tags_flags_count]

        for _ in range(tags_count):
            red_flag_tag = RedFlagTag()
            red_flag_tag.rel_creator = random.choice(User.query.filter(User.id != 0).all())
            red_flag_tag.rel_to_tag = random.choice(Tag.query.all())
            db.session.add(red_flag_tag)
        print("Tags red flags created")

    def generate_users_red_flags(self):
        users_count = self.objects_count_dict[self.str_users_flags_count]

        for _ in range(users_count):
            red_flag_user = RedFlagUser()
            red_flag_user.rel_creator = random.choice(User.query.filter(User.id != 0).all())
            red_flag_user.rel_to_user = random.choice(User.query.filter(User.id != red_flag_user.rel_creator.id).all())
            db.session.add(red_flag_user)
        print("Users red flags created")
