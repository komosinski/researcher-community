from open_science import db, app
from open_science.models import create_essential_data
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


# drops all tables from database not relying on models
def drop_all_from_database():
    connection = db.engine.connect()
    connection.execute('DROP SCHEMA public CASCADE')
    connection.execute('CREATE SCHEMA public')


init_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if not database_exists(init_engine.url):
    create_database(init_engine.url)

db.drop_all()
db.create_all()
db.session.commit()

create_essential_data()
