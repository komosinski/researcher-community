from open_science.models import ReviewRequest, Review
from open_science import app, db
from open_science.enums import UserTypeEnum, EmailTypeEnum,\
     NotificationTypeEnum
import open_science.email as em
import datetime as dt
from open_science.notification.helpers import create_notification
from flask.helpers import url_for


def create_review_request(reviewer, paper_revision):

    review_request = ReviewRequest(
        creation_datetime=dt.datetime.utcnow(),
        deadline_date=dt.datetime.utcnow().date() + dt.timedelta(days=30)
    )
    review_request.rel_requested_user = reviewer
    review_request.rel_related_paper_version = paper_revision
    db.session.add(review_request)
    db.session.commit()

    em.send_review_request(reviewer.email, paper_revision.abstract,
                           review_request.id)
    em.insert_email_log(0, reviewer.id, reviewer.email,
                        EmailTypeEnum.REVIEW_REQUEST.value)

    create_notification(NotificationTypeEnum.REVIEW_REQUEST.value,
                        'You have new review request',
                        reviewer,
                        url_for('review_request_page',
                                request_id=review_request.id))


def select_reviewers(paper_revision):

    # TODO: replace this with users from text_processing module
    users = paper_revision.get_similar_users()
    potential_reviewers = []
  
    # for each author of this paper, all co-authors of their papers
    # from the last n days are removed
    creators = paper_revision.rel_creators
    co_authors_ids = set()
    days = app.config['EXCLUDE_CO_AUTHOR_FOR_REVIEW_DAYS']

    # those for whom the current authors reviewed any paper within n-days
    # are removed
    reviewed_users_ids = set()

    for creator in creators:
        for paper_revision in creator.rel_created_paper_revisions:
            ids = paper_revision.get_paper_co_authors_ids(days)
            if isinstance(ids, int):
                co_authors_ids.add(ids)
            else:
                co_authors_ids \
                    .update(ids)

        ids = creator\
            .get_users_ids_whose_user_reviewed(
                app
                .config['EXCLUDE_REVIEWED_AUTHOR_FOR_REVIEW_DAYS']
                )

        if isinstance(ids, int):
            reviewed_users_ids.add(ids)
        else:
            reviewed_users_ids.update(ids)
    # Users who declined to review this paper are removed.
    # except users who declined with reason "don't have time"
    # more than N days ago
    paper_revisions = [rev for rev in
                       paper_revision.rel_parent_paper.rel_related_versions]
    users_who_declined_ids = set()
    for revision in paper_revisions:
        for request in revision.rel_related_review_requests:
            if request.decision is False and\
                    request.can_request_after_decline() is False:
                users_who_declined_ids.add(request.requested_user)

    # If a new revision of the paper needs to be reviewed,
    # first the reviewers of previous revision(s) are asked
    previous_reviewers = []
    previous_reviewers_ids = set()
    if paper_revision.version > 1:
        for revision in paper_revision.get_previous_revisions():
            for review in revision.rel_related_reviews:
                previous_reviewers_ids.add(review.creator)

    for user in users:
        if user.is_active() is False:
            continue
        elif user.privileges_set != UserTypeEnum.RESEARCHER_USER.value:
            continue
        elif user.id in [creator.id for creator in creators]:
            continue
        elif user.get_current_review_mails_limit() == 0:
            continue
        elif user.id in [request.requested_user for request in
                         paper_revision
                         .rel_related_review_requests]:
            continue
        elif user.id in co_authors_ids:
            continue
        elif user.id in users_who_declined_ids:
            continue
        elif user.id in reviewed_users_ids:
            continue
        elif user.id in previous_reviewers_ids:
            previous_reviewers.append(user)
        else:
            potential_reviewers.append(user)

    potential_reviewers.sort(key=lambda x: x.get_review_workload())

    if not previous_reviewers:
        return potential_reviewers
    else:
        previous_reviewers.sort(key=lambda x: x.get_review_workload())
        return previous_reviewers + potential_reviewers


# returns False is there are not enough researchers with similar profiles
# in the system to review this paper revision
def prepare_review_requests(paper_revision):

    missing_count = paper_revision.get_missing_reviewers_count()

    if missing_count <= 0:
        return True

    potential_reviewers = select_reviewers(paper_revision)

    if not potential_reviewers:
        return False

    for potential_reviewer in potential_reviewers:
        create_review_request(potential_reviewer, paper_revision)
        missing_count -= 1
        if missing_count == 0:
            return True

    return False


# binds unpublished reviews and unanswered review reqests
# to newest paper's revision
def transfer_old_reviews(paper):
    latest_revision = paper.get_latest_revision()
    if latest_revision.version > 1:
        reviews_to_transfer = []
        review_requests_to_transfer = []
        # check already requested users in latest_revision
        requested_reviewers_ids = [review_r.requested_user for
                                   review_r in latest_revision
                                   .rel_related_review_requests]
        for revision in paper.rel_related_versions:
            if revision.version == 1:
                continue
            for review_request in revision.rel_related_review_requests:
                if review_request.decision is True:
                    review = Review.query\
                        .filter(Review.creator
                                == review_request.requested_user,
                                Review.related_paper_version
                                == review_request
                                .paper_version)\
                        .first()
                    if review and review.publication_datetime is None:
                        reviews_to_transfer.append(review)
                elif review_request.decision is None:
                    review_requests_to_transfer.append(review_request)

        for review in reviews_to_transfer:
            if review.creator not in requested_reviewers_ids:
                # bind review to new revision
                review.rel_related_paper_version = latest_revision
                # create notification
                create_notification(NotificationTypeEnum.REVIEW_TRANSFER.value,
                                    'The review has been transferred \
                                        to new paper\'s revision',
                                    review.creator,
                                    url_for('article',
                                            id=paper.id,
                                            version=revision.version))

        for review_request in review_requests_to_transfer:
            if review_request.requested_user not in requested_reviewers_ids:
                # bind review_request to new revision
                review_request.rel_related_paper_version = latest_revision

        db.session.commit()
