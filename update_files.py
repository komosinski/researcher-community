from data_generator.data_generator import DataGenerator
from open_science import app
from open_science.models import License


def update_files():

    data_generator = DataGenerator(app)
    is_created = data_generator.create_text_processing_data()
    
    if is_created:
        print("Text processing data have been created")
    else:
        print("Text processing data have not been completely created")

    License.insert_missing_licenses()

update_files()
