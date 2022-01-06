from open_science import db
from open_science.models import  Tag, Review, Comment, PaperRevision
from flask_login import current_user
from flask import request

def user_papers_data():
    
   #TODO: Use current_user.id() to get only user's papers

    query = PaperRevision.query
    total_results = query.count()

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            PaperRevision.title.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['version']:
            col_name = 'version'
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

    # response
    return {
        'data': [paper.to_dict() for paper in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_results,
        'draw': request.args.get('draw', type=int),
    }


def user_reviews_data():
    
    query = Review.query.filter(Review.creator == current_user.id)
    total_results = query.count()

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Review.text.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
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
  
    # response
    return {
        'data': [review.to_dict() for review in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_results,
        'draw': request.args.get('draw', type=int),
    }



def user_tags_data():
    
    query = Tag.query.filter(Tag.creator == current_user.id)
    total_results = query.count()

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Tag.name.like(f'%{search.upper()}%'),
            Tag.description.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['deadline']:
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
  
    # response
    return {
        'data': [tag.to_dict() for tag in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_results,
        'draw': request.args.get('draw', type=int),
    }



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

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['date']:
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
  
    # response
    return {
        'data': [comment.to_dict() for comment in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_results,
        'draw': request.args.get('draw', type=int),
    }

