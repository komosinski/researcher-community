# Private sources of the openscience project.

Introduction
------------

First setup
------------

  1. Move to main directory and create python virtual env

    python3 -m venv venv
  
  2. Activate virtual env

    Linux
      $ source venv/bin/activate
      (venv) $ _
 
    Windows 
      $ venv\Scripts\activate
      (venv) $ _
 
  3. Install requirements
  
    pip install -r requirements.txt
  
  4. (Temporary step*) Create temporary_config.py file in main directory with must contain the following code:

    DATABASE_URI = 'postgresql://USER:PASSWORD@localhost:5432/DB'
  
  5. Create tables in DB

    Start the Python interpreter and write:
  
      from open_science import db
      db.create_all()
      db.session.commit()
      exit()

Run
------------

In your virtual env type:

    flask run
  
Initializing test data
------------

Go to http://127.0.0.1:5000/t to initiate test records in the database 