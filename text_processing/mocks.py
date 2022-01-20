from open_science.models import User, PrivilegeSet

def get_potential_reviewers(paper_version_id):
  
    # paper = PaperRevision.query.filter(PaperRevision.id == paper_version_id).first()
    # query_authors = db.session.query(User.id) 
    # reviewers = User.query.filter(User.privileges_set == scientific_id ,User.id.not_in(query_authors)).all() 

    scientific_id = PrivilegeSet.query.filter(PrivilegeSet.id==User.user_types_enum.RESEARCHER_USER.value).first().id
    reviewers = User.query.filter(User.privileges_set == scientific_id).all() 

    return reviewers

def get_text(url):
    return "Lorem ipsum tralala"