from data_generator.data_generator import DataGenerator
from open_science import app


def update_files():

    data_generator = DataGenerator(app)
    is_created = data_generator.create_text_processing_data()
    
    if is_created:
        print("Text processing data have been created")
    else:
        print("Text processing data have not been completely created")

    data_generator.update_licenses()

update_files()
