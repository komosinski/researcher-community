from open_science import db
from open_science.models import Tag
from flask import request

def get_all_tags_data():

    query = Tag.query
    total_results = query.count()

    # search filter and sorting
    search = request.args.get('search[value]')
    if search:
        query = query.filter(Tag.name.like(f'%{search.upper()}%')).order_by(Tag.name.asc())

    total_filtered = query.count()

    return {
        'data': [tag.to_dict() for tag in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': total_results,
        'draw': request.args.get('draw', type=int),
    }

