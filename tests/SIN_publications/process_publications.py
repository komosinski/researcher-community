import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parent_parentdir =  os.path.dirname(parentdir)
sys.path.insert(0, parent_parentdir) 

import csv
from open_science import db
from open_science.models import User, CalibrationPaper
from text_processing.prepocess_text import preprocess_text

def get_file_name():
    file_name = 'publications-2018-2024-output.csv'
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    return file_name

def load_file():

    file_name = get_file_name()
    users_list = []
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        users_list = list(csv_reader)
        print(f'Loaded {len(users_list)} users')
        print(f'Colum names: {users_list[0].keys()}') 
     
    return users_list

def insert_calibration_paper(user, user_dict):
    calibration_paper = CalibrationPaper(
                pdf_url="",
                preprocessed_text= preprocess_text(user_dict['PublishedText']),
                description = user_dict['ID'] + user_dict['PublishedText'][:50]
                )
    db.session.add(calibration_paper)
    user.rel_calibration_papers.append(calibration_paper)

def insert_users_and_calibration_papers(users_dict_list):
    count = len(users_dict_list)
    for i,user_dict in enumerate(users_dict_list):
            user = User(
                first_name=user_dict['FirstName'],
                second_name=user_dict['SecondName'],
                email=f"{user_dict['ID']}@email.pl",
                plain_text_password="6e2e3c28-5c1d"
            )
            db.session.add(user)
            db.session.flush()
            insert_calibration_paper(user, user_dict)
            if i % 100 == 0:
                 print(f'{(i/count)*100:.1f} %') 

    db.session.commit()
    print('Users and calibration papers have been inserted')

users_dict_list = load_file()
insert_users_and_calibration_papers(users_dict_list)


