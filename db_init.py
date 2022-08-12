from data_generator.data_generator import DataGenerator
from open_science import db, app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


def db_init():
    init_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(init_engine.url):
        create_database(init_engine.url)

    db.drop_all()
    db.create_all()
    db.session.commit()

    # we pass counts_overwrite_dict to DataGenerator to generate smaller database faster
    # for real amount of data remove counts_overwrite_dict attribute
    counts_overwrite_dict = {
        DataGenerator.str_users_count: 50,
        DataGenerator.str_papers_count: 10,
        DataGenerator.str_revisions_count: 10,
        DataGenerator.str_reviews_count: 10,
        DataGenerator.str_tags_count: 10,
        DataGenerator.str_comments_count: 10,
        DataGenerator.str_review_requests_count: 10,
        DataGenerator.str_votes_count: 10,
        DataGenerator.str_staff_messages_count: 10,
        DataGenerator.str_notifications_count: 10,
        DataGenerator.str_suggestions_count: 10,
        DataGenerator.str_calibration_papers_count: 10,
        DataGenerator.str_changes_components_count: 10,
        DataGenerator.str_comments_flags_count: 10,
        DataGenerator.str_revisions_flags_count: 10,
        DataGenerator.str_reviews_flags_count: 10,
        DataGenerator.str_tags_flags_count: 10,
        DataGenerator.str_users_flags_count: 10
    }
    data_generator = DataGenerator(app, counts_overwrite_dict)
    data_generator.generate_data()
    data_generator.create_text_processing_data()

    print("db_init ended successfully")


db_init()


# drops all tables from database not relying on models
def drop_all_from_database():
    connection = db.engine.connect()
    connection.execute('DROP SCHEMA public CASCADE')
    connection.execute('CREATE SCHEMA public')
