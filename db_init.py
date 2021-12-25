from open_science import db
db.create_all()
db.session.commit()

from open_science.models import create_essential_data 
create_essential_data()