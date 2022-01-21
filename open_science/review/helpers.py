from open_science.models import User, ReviewRequest
from open_science import app, db
from open_science.enums import UserTypeEnum, EmailTypeEnum, NotificationTypeEnum
import open_science.email as em
import datetime as dt
from open_science.notification.helpers import create_notification
from flask.helpers import url_for

NOT_ENOUGHT_RESEARCHERS_TEXT = 'There are not enough researchers with similar research profiles\
in the system to review this paper. We will wait until more similar researchers are\
        available. You can help with peer review by inviting your colleagues to join [sitename]!'

def create_review_request(reviewer, paper_revision):

    review_request = ReviewRequest(
        creation_datetime=dt.datetime.utcnow()
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
    users = User.query.all()

    potential_reviewers = []

    # for each author of this paper, all co-authors of their papers 
    # from the last n days are removed
    creators = paper_revision.rel_creators
    co_authors_ids = set()
    days = app.config['EXCLUDE_CO_AUTHOR_FOR_REVIEW_DAYS']

    #those for whom the current authors reviewed any paper within n-days
    # are removed
    reviewed_users_ids = set()

    for creator in creators:
        for paper_revision in creator.rel_created_paper_revisions:
            co_authors_ids \
                .update(paper_revision.get_paper_co_authors_ids(days))
 
        ids = creator\
            .get_users_ids_whose_user_reviewed(
                app
                .config['EXCLUDE_REVIEWED_AUTHOR_FOR_REVIEW_DAYS']
                )

        reviewed_users_ids.update(ids)
        
    # Users who declined to review this paper are removed.
    paper_revisions_ids = [rev.id for rev in paper_revision.rel_parent_paper.rel_related_versions]
    paper_review_requests = ReviewRequest \
        .query \
        .filter(ReviewRequest.requested_user.in_(paper_revisions_ids),
                ReviewRequest.decision.is_(False)).all()

    users_who_declined_ids = set([rev.id for rev in paper_review_requests])

    # If a new revision of the paper needs to be reviewed,
    # first the reviewers of previous revision(s) are asked
    previous_reviewers = []
    previous_reviewers_ids = set()
    if paper_revision.version > 1:
        for revision in paper_revision.get_previous_revisions():
            for review in revision.rel_related_reviews:
                previous_reviewers_ids.update(review.creator)

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
