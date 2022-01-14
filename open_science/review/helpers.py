from open_science.models import User, ReviewRequest
from open_science import app, db
from open_science.enums import UserTypeEnum, EmailTypeEnum
import open_science.email as em
import datetime as dt
from open_science.notification.helpers import create_notification


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
    
    em.send_review_request(reviewer.email, paper_revision.abstract, review_request.id)
    em.insert_email_log(0, reviewer.id, reviewer.email, EmailTypeEnum.REVIEW_REQUEST.value)


def select_reviewers(paper_revision):

    # TODO: replace this with users from text_processing module
    users = User.query.all()

    potential_reviewers = []

    # for each author of this paper, all co-authors of their papers 
    # from the last n days are removed
    creators = paper_revision.rel_creators
    co_authors_ids = set()
    days = app.config('EXCLUDE_CO_AUTHOR_FOR_REVIEW_DAYS')
    for creator in creators:
        for paper_revision in creator.rel_created_paper_revisions:
            co_authors_ids \
                .update(paper_revision.get_paper_co_authors_ids(days))

    # Users who declined to review this paper are removed.
    paper_revisions_ids = [rev.id for rev in paper_revision.rel_parent_paper.rel_related_versions]
    paper_review_requests = ReviewRequest \
        .query \
        .filter(ReviewRequest.requested_user.in_(paper_revisions_ids),
                ReviewRequest.decision.is_(False)).all()

    users_who_declined_ids = set([rev.id for rev in paper_review_requests])

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
                        paper_revision.rel_related_review_requests]:
            continue
        elif user.id in co_authors_ids:
            continue
        elif user.id in users_who_declined_ids:
            continue
        else:
            potential_reviewers.append(user)

    potential_reviewers.sort(key=lambda x: x.get_review_workload())

    return potential_reviewers


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
