from operator import and_

from sqlalchemy import func

from open_science.db_helper import get_hidden_filter
from open_science.models import User, Tag, PaperRevision
from open_science import db

pv_hidden_filter = get_hidden_filter(PaperRevision)

subq_max_versions = (db.session.query(PaperRevision.parent_paper,
                                      func.max(PaperRevision.version).label("max_version"))
                     .group_by(PaperRevision.parent_paper)
                     ).subquery()


def get_paper_order(order_by):
    if order_by == 'newest':
        order = PaperRevision.publication_date.desc()
    elif order_by == 'oldest':
        order = PaperRevision.publication_date.asc()
    else:
        order = PaperRevision.publication_date.desc()
    return order


def get_papers_basic_search(search_like, search_option, order, page_num, rows_per_page):
    paper_revisions = []

    paper_revisions = PaperRevision.query \
        .options(db.defer('preprocessed_text')) \
        .join(subq_max_versions, and_(PaperRevision.parent_paper == subq_max_versions.c.parent_paper,
                                      PaperRevision.version == subq_max_versions.c.max_version)) \
        .filter(pv_hidden_filter)

    if search_like == '%%':
        pass
    elif search_option == 'title':
        paper_revisions = paper_revisions \
            .filter(PaperRevision.title.ilike(search_like))
    elif search_option == 'description':
        paper_revisions = paper_revisions \
            .filter(PaperRevision.abstract.ilike(search_like))
    elif search_option == 'author':
        paper_revisions = paper_revisions \
            .join(User, PaperRevision.rel_creators) \
            .filter((User.first_name.ilike(search_like))
                    | (User.second_name.ilike(search_like))) \
            .group_by(PaperRevision.id)
    elif search_option == 'text':
        paper_revisions = paper_revisions \
            .filter(PaperRevision.preprocessed_text.ilike(search_like))
    elif search_option == 'all':
        paper_revisions = paper_revisions \
            .filter((PaperRevision.title.ilike(search_like))
                    | (PaperRevision.abstract.ilike(search_like))
                    | (PaperRevision.preprocessed_text.ilike(search_like)))

    paper_revisions = paper_revisions \
        .order_by(order) \
        .paginate(page=page_num, per_page=rows_per_page)

    return paper_revisions


def get_user_order(order_by):
    order = User.reputation.desc()
    return order


def get_tag_order(order_by):
    order = Tag.name.asc()
    return order


def get_papers_advanced_search(page, search_data, order):
    paper_revisions = []

    paper_revisions = PaperRevision.query \
        .options(db.defer('preprocessed_text')) \
        .filter(pv_hidden_filter)

    if 'show_all' in search_data:
        show_all = bool(search_data['show_all'])
    else:
        show_all = False

    if not show_all:
        paper_revisions = paper_revisions \
            .join(subq_max_versions, and_(PaperRevision.parent_paper == subq_max_versions.c.parent_paper,
                                          PaperRevision.version == subq_max_versions.c.max_version))

    if 'title' in search_data and search_data['title'] != '':
        paper_revisions = paper_revisions \
            .filter(PaperRevision.title.ilike("%{}%".format(search_data['title'])))
    if 'text' in search_data and search_data['text'] != '':
        paper_revisions = paper_revisions \
            .filter(PaperRevision.preprocessed_text.ilike("%{}%".format(search_data['text'])))
    if 'author' in search_data and search_data['author'] != '':
        paper_revisions = paper_revisions \
            .join(User, PaperRevision.rel_creators) \
            .filter((User.first_name.ilike("%{}%".format(search_data['author'])))
                    | (User.second_name.ilike("%{}%".format(search_data['author'])))) \
            .group_by(PaperRevision.id)
    if 'tag' in search_data and search_data['tag'] != '':
        paper_revisions = paper_revisions \
            .join(Tag, PaperRevision.rel_related_tags) \
            .filter(Tag.name.ilike("%{}%".format(search_data['tag']))) \
            .group_by(PaperRevision.id)

    if 'per_page' in search_data:
        per_page = int(search_data['per_page'])
    else:
        per_page = 5

    paper_revisions = paper_revisions \
        .order_by(order) \
        .paginate(page=page, per_page=per_page)

    return paper_revisions


def get_users_advanced_search(page, search_data, order):
    users = []

    user_hidden_filter = get_hidden_filter(User)

    users = db.session.query(User.id,
                             User.first_name,
                             User.second_name,
                             User.affiliation,
                             User.email) \
        .filter(user_hidden_filter
                & (User.id != 0)  # don't show site user
                & (User.privileges_set != 30))  # don't show admin users

    if 'first_name' in search_data and search_data['first_name'] != '':
        users = users \
            .filter(User.first_name.ilike("%{}%".format(search_data['first_name'])))
    if 'second_name' in search_data and search_data['second_name'] != '':
        users = users \
            .filter(User.second_name.ilike("%{}%".format(search_data['second_name'])))
    if 'affiliation' in search_data and search_data['affiliation'] != '':
        users = users \
            .filter(User.affiliation.ilike("%{}%".format(search_data['affiliation'])))
    if 'orcid' in search_data and search_data['orcid'] != '':
        users = users \
            .filter(User.orcid.ilike("%{}%".format(search_data['orcid'])))
    if 'tag' in search_data and search_data['tag'] != '':
        users = users \
            .join(Tag, User.rel_tags_to_user) \
            .filter(Tag.name.ilike("%{}%".format(search_data['tag']))) \
            .group_by(User.id)

    if 'per_page' in search_data:
        per_page = int(search_data['per_page'])
    else:
        per_page = 5

    users = users \
        .order_by(order) \
        .paginate(page=page, per_page=per_page)

    return users


def get_tags_advanced_search(page, search_data, order):
    tags = []

    tags_hidden_filter = get_hidden_filter(Tag)

    tags = db.session.query(Tag.id,
                            Tag.name,
                            Tag.deadline,
                            Tag.description, ) \
        .filter(tags_hidden_filter)

    if 'name' in search_data and search_data['name'] != '':
        tags = tags \
            .filter(Tag.name.ilike("%{}%".format(search_data['name'])))
    if 'description' in search_data and search_data['description'] != '':
        tags = tags \
            .filter(Tag.description.ilike("%{}%".format(search_data['description'])))

    if 'per_page' in search_data:
        per_page = int(search_data['per_page'])
    else:
        per_page = 5

    tags = tags \
        .order_by(order) \
        .paginate(page=page, per_page=per_page)

    return tags
