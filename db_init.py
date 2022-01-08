from open_science import db
from open_science.models import create_essential_data


# drops all tables from database not relying on models
def drop_all_from_database():
    connection = db.engine.connect()
    connection.execute('DROP SCHEMA public CASCADE')
    connection.execute('CREATE SCHEMA public')


drop_all_from_database()
db.create_all()
db.session.commit()

create_essential_data()
