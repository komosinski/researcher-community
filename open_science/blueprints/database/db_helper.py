from operator import and_, or_
from sqlalchemy import func, true, false
from open_science import db
from flask import current_app
from open_science.models import PaperRevision, Review, CalibrationPaper
from text_processing.search_engine import search_articles_by_text


# returns paper versions with not enough reviews
def get_missing_reviews_pvs(page_num, rows_per_page):
    subq_max_versions = (db.session.query(PaperRevision.parent_paper,
                                          func.max(PaperRevision.version).
                                          label("max_version"))
                         .group_by(PaperRevision.parent_paper)
                         ).subquery()

    subq_reviews_count = (
        db.session.query(PaperRevision.id, func.count(Review.publication_datetime).label("reviews_count"))
            .join(Review, isouter=True)
            .join(subq_max_versions, and_(PaperRevision.parent_paper == subq_max_versions.c.parent_paper,
                                          PaperRevision.version == subq_max_versions.c.max_version))
            .group_by(PaperRevision.id)
            .order_by(PaperRevision.id)
    ).subquery()

    paper_revisions = db.session.query(PaperRevision) \
        .join(subq_reviews_count, and_(PaperRevision.id == subq_reviews_count.c.id,
                                       PaperRevision.confidence_level > subq_reviews_count.c.reviews_count)) \
        .order_by(PaperRevision.id) \
        .paginate(page=page_num, per_page=rows_per_page)

    return paper_revisions


# returns true if item is not hidden by exceeding the red flags limit
# handles force_show and force_hide
def can_show_object(item):
    if item.force_show and item.force_hide:
        raise ValueError("Both force_show and force_hide values can't be true")
    elif item.force_show:
        return True
    elif item.force_hide:
        return False
    else:
        return item.red_flags_count < current_app.config['RED_FLAGS_THRESHOLD']


# returns filter for hidden items based on red flags, force hide and force 
# show for given class
def get_hidden_filter(item_class):
    return and_(or_(item_class.force_show == true(),
                    item_class.red_flags_count < current_app.config['RED_FLAGS_THRESHOLD']),
                item_class.force_hide == false())


# returns filter for matching paper revisions by search_text
# paper_revisions_query -> current query
def get_search_by_text_filter(search_text):
    matched_papers_ids = [int(id) for id in search_articles_by_text(search_text)]
    return PaperRevision.id.in_(matched_papers_ids)
