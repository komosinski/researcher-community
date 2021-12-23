from open_science import *
from open_science.test_data import create_essential_data

#Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(debug=True)
    create_essential_data()