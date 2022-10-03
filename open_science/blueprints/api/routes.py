from open_science.blueprints.api import bp
from flask import current_app as app
from flask_login import login_required
from open_science.models import Tag, Review, Comment, PaperRevision, User
from flask import request
from open_science import db
from flask_login import current_user
from open_science.utils import researcher_user_required
from open_science.enums import UserTypeEnum


@bp.route('/api/tags')
def get_all_tags_data():

    query = Tag.query
    total_results = query.count()

    # search filter and sorting
    search = request.args.get('search[value]')
    if search:
        query = query.filter(Tag.name.like(f'%{search.upper()}%'))\
            .order_by(Tag.name.asc())

    total_filtered = query.count()

    return {
        'data': [tag.to_dict() for tag in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_results,
        'draw': request.args.get('draw', type=int),
    }



@bp.route('/api/user_papers')
@login_required
@researcher_user_required
def user_papers_data():
    query = PaperRevision.query \
        .join(User, PaperRevision.rel_creators) \
        .filter(User.id == current_user.id)

    total_results = query.count()

    # search filters
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            PaperRevision.title.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting by one or more attributes
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['version', 'title', 'publication_date']:
            col_name = 'publication_date'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(PaperRevision, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    return {
        'data': [paper.to_dict() for paper in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_results,
        'draw': request.args.get('draw', type=int),
    }



@bp.route('/api/user_reviews')
@login_required
@researcher_user_required
def user_reviews_data():

    query = Review.query.filter(Review.creator == current_user.id)
    total_results = query.count()

    # search filters
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Review.text.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting by one or more attributes
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['publication_datetime']:
            col_name = 'publication_datetime'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Review, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    return {
        'data': [review.to_dict() for review in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_results,
        'draw': request.args.get('draw', type=int),
    }


@bp.route('/api/user_tags')
@login_required
@researcher_user_required
def user_tags_data():

    query = Tag.query.filter(Tag.creator == current_user.id)
    total_results = query.count()

    # search filters
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Tag.name.like(f'%{search.upper()}%'),
            Tag.description.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting by one or more attributes
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['deadline', 'name', 'description']:
            col_name = 'deadline'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Tag, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    return {
        'data': [tag.to_dict() for tag in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_results,
        'draw': request.args.get('draw', type=int),
    }


@bp.route('/api/user_comments')
@login_required
def user_comments_data():

    query = Comment.query.filter(Comment.creator == current_user.id)
    total_results = query.count()

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Comment.text.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting by one or more attributes
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['date', 'text', 'votes_score']:
            col_name = 'date'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Comment, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    return {
        'data': [comment.to_dict() for comment in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_results,
        'draw': request.args.get('draw', type=int),
    }



@bp.route('/api/users')
def get_users():

    args = request.args
    query = '%' + args.get('q') + '%'
  
    page = args.get('page')
    if page.isdigit():
        page = int(page)
    else:
        page = 1 

    users = User.query.filter((User.privileges_set == UserTypeEnum.RESEARCHER_USER.value) &
                              ((User.first_name.ilike(query)) |
                              (User.second_name.ilike(query)) |
                              (User.affiliation.ilike(query)))).order_by(User.first_name).paginate(page, app.config['AJAX_SELECT_SEARCH_RESULTS'] , False)

    return {
        'results': [user.to_dict() for user in users.items],
         'pagination': {
            'more': True if app.config['AJAX_SELECT_SEARCH_RESULTS']*page < users.total else False
         }
    }