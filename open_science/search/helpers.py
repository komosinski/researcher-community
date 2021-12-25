from open_science.models import Paper, User, Tag
from open_science import db

#TODO: #Posiuu complete helpers-->

def get_paper_order(order_by):
   
    # if order_by=='newest':
    #     order = Paper.publication_date.desc()
    # elif order_by=='oldest':
    #     order = Paper.publication_date.asc()
    # elif order_by=='score':
    #     order = Paper.votes_score.desc()
    # else:
    #     order = Paper.publication_date.desc()
    order = Paper.votes_score.desc()
    return order

def get_papers_basic_search(search_like, search_option, order,page_num, rows_per_page):

    papers = []

    if search_like == '%%':
        papers =  db.session.query(Paper.id,Paper.title,Paper.description,Paper.publication_date).order_by(order).paginate(page=page_num, per_page=rows_per_page)
    elif search_option=='title':
        papers = db.session.query(Paper.id,Paper.title,Paper.description,Paper.publication_date).filter(Paper.title.ilike(search_like)).order_by(order).paginate(page=page_num, per_page=rows_per_page)
    elif search_option=='description':
        papers = db.session.query(Paper.id,Paper.title,Paper.description,Paper.publication_date).filter(Paper.description.ilike(search_like)).order_by(order).paginate(page=page_num, per_page=rows_per_page)
    elif search_option=='author':
        #TODO: Write this query
        #papers = Paper.query(Paper).join(Paper.rel_creators).filter(Paper.rel_creators.namelike(search_like)).order_by(order).paginate(page=page_num, per_page=rows_per_page)
        papers = db.session.query(Paper.id,Paper.title,Paper.description,Paper.publication_date).order_by(order).paginate(page=page_num, per_page=rows_per_page) #temporary query
    elif search_option=='text':
        papers = db.session.query(Paper.id,Paper.title,Paper.description,Paper.publication_date).filter(Paper.text.ilike(search_like)).order_by(order).paginate(page=page_num, per_page=rows_per_page)
    elif search_option=='all':
        papers = db.session.query(Paper.id,Paper.title,Paper.description,Paper.publication_date).filter((Paper.title.ilike(search_like))|(Paper.description.ilike(search_like))|(Paper.text.ilike(search_like))).order_by(order).paginate(page=page_num, per_page=rows_per_page)
    
    return papers

def get_user_order(order_by):
   
    order = User.reputation.desc()
    return order

def get_tag_order(order_by):
   
    order = Tag.name.asc()
    return order

def get_papers_advanced_search(page, search_data, order):
    papers = []
    search_options = dict()
    
    if 'per_page' in search_data:
        per_page = int(search_data['per_page'])
    else:
        per_page = 5


    if 'user' in search_data:
        search_options['user'] = search_data['user']
    if 'title' in search_data:
        search_options['title'] = search_data['title']
    # etc.. or do it another way

    if 'search_text' in search_data:
        search_text = search_data['search_text']
    else:
        search_text = ''
    #TODO: make query with filters in search_options

    search_like = "%{}%".format(search_text)

    if 'user_id' in search_data:
        pass

    # TEMPORARY QUERY
    papers =  db.session.query(Paper.id,Paper.title,Paper.description,Paper.publication_date).order_by(order).paginate(page=page, per_page=per_page)

    return papers

def get_users_advanced_search(page, search_data, order):
    users = []
    search_options = dict()

    if 'per_page' in search_data:
        per_page = int(search_data['per_page'])
    else:
        per_page = 5

    if 'search_text' in search_data:
        search_text = search_data['search_text']
    else:
        search_text = ''

    search_like = "%{}%".format(search_text)

    # TEMPORARY QUERY
    users =  db.session.query(User.first_name,User.second_name,User.reputation,User.orcid,User.id,User.has_photo).filter(User.confirmed==True).order_by(order).paginate(page=page, per_page=per_page)
    
    return users


def get_tags_advanced_search(page, search_data, order):
    tags = []
   
    if 'per_page' in search_data:
        per_page = int(search_data['per_page'])
    else:
        per_page = 5

    if 'search_text' in search_data:
        search_text = search_data['search_text']
    else:
        search_text = ''

    search_like = "%{}%".format(search_text)

    # TEMPORARY QUERY
    tags = db.session.query(Tag.name).order_by(order).paginate(page=page, per_page=per_page)
    
    return tags