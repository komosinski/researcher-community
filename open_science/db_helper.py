from operator import and_

from sqlalchemy import func

from open_science import db
from open_science.models import PaperVersion, Review


# returns paper versions with not enough reviews
def get_missing_reviews_pvs(page_num, rows_per_page):
    subq_max_versions = (db.session.query(PaperVersion.parent_paper,
                                          func.max(PaperVersion.version).label("max_version"))
                         .group_by(PaperVersion.parent_paper)
                         ).subquery()

    subq_reviews_count = (db.session.query(PaperVersion.id, func.count(Review.publication_datetime).label("reviews_count"))
                          .join(Review, isouter=True)
                          .join(subq_max_versions, and_(PaperVersion.parent_paper == subq_max_versions.c.parent_paper,
                                                        PaperVersion.version == subq_max_versions.c.max_version))
                          .group_by(PaperVersion.id)
                          .order_by(PaperVersion.id)
                          ).subquery()

    paper_versions = db.session.query(PaperVersion)\
        .join(subq_reviews_count, and_(PaperVersion.id == subq_reviews_count.c.id,
                                       PaperVersion.confidence_level > subq_reviews_count.c.reviews_count))\
        .order_by(PaperVersion.id)\
        .paginate(page=page_num, per_page=rows_per_page)

    return paper_versions
