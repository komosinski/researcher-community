from operator import and_

from sqlalchemy import func

from open_science import db
from open_science.models import PaperRevision, Review


# returns paper versions with not enough reviews
def get_missing_reviews_pvs(page_num, rows_per_page):
    subq_max_versions = (db.session.query(PaperRevision.parent_paper,
                                          func.max(PaperRevision.version).label("max_version"))
                         .group_by(PaperRevision.parent_paper)
                         ).subquery()

    subq_reviews_count = (db.session.query(PaperRevision.id, func.count(Review.publication_datetime).label("reviews_count"))
                          .join(Review, isouter=True)
                          .join(subq_max_versions, and_(PaperRevision.parent_paper == subq_max_versions.c.parent_paper,
                                                        PaperRevision.version == subq_max_versions.c.max_version))
                          .group_by(PaperRevision.id)
                          .order_by(PaperRevision.id)
                          ).subquery()

    paper_versions = db.session.query(PaperRevision)\
        .join(subq_reviews_count, and_(PaperRevision.id == subq_reviews_count.c.id,
                                       PaperRevision.confidence_level > subq_reviews_count.c.reviews_count))\
        .order_by(PaperRevision.id)\
        .paginate(page=page_num, per_page=rows_per_page)

    return paper_versions
