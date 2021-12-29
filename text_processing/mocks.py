from open_science.extensions import db
from open_science import app
from open_science.models import User, PaperVersion, PrivilegeSet

def get_potential_reviewers(paper_version_id):
  
    # paper = PaperVersion.query.filter(PaperVersion.id == paper_version_id).first()
    # query_authors = db.session.query(User.id) 
    # reviewers = User.query.filter(User.privileges_set == scientific_id ,User.id.not_in(query_authors)).all() 

    scientific_id = PrivilegeSet.query.filter(PrivilegeSet.name=='scientific_user').first().id
    reviewers = User.query.filter(User.privileges_set == scientific_id).all() 

    return reviewers

  