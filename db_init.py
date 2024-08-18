from data_generator.data_generator import DataGenerator
from open_science import db, app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


# drops all tables from the database not relying on the models defined in the source - deletes everything
def drop_all_from_database():
    connection = db.engine.connect()
    connection.execute('DROP SCHEMA public CASCADE')
    connection.execute('CREATE SCHEMA public')


def db_init():
    init_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(init_engine.url):
        create_database(init_engine.url)

    CLEAR_ALL = True  # delete everything from the database? useful when the model defined in the source has changed compared to the current database content
    if CLEAR_ALL:
        drop_all_from_database()
    else:
        db.drop_all()  # drops tables from the database according to the models defined in the source
    db.create_all()
    db.session.commit()

    data_generator = DataGenerator(app)
    data_generator.create_essential_data()
    data_generator.create_text_processing_data()

    print("db_init ended successfully")


db_init()
