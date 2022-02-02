from open_science import db, app
from open_science.models import create_essential_data
import text_processing.similarity_matrix as sm
from text_processing.plot import create_save_users_plot
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

dictionary = sm.create_dictionary()
sm.save_dictionary(dictionary)
tfidf_matrix = sm.create_tfidf_matrix()
sm.save_tfidf_matrix(tfidf_matrix)
similarities_matrix = sm.create_similarities_matrix()
sm.save_similarities_matrix(similarities_matrix)
create_save_users_plot()
print("db_init ended successfully")
