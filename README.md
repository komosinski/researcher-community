# Private sources of the openscience project.

Introduction
------------

First setup
------------

      
  1. Install poppler on your local machine
  
    Linux  
      $ sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev
      
    Windows
      $ conda install -c conda-forge poppler
      
  2. Move to main directory and create python virtual env

    python3 -m virtualenv venv
  
  3. Activate virtual env

    Linux
      $ source venv/bin/activate
 
    Windows 
      $ venv\Scripts\activate
 
  4. Install requirements
  
    pip install -r requirements.txt
  
  5. (Temporary step*) Create temporary_config.py file in main directory which must contain database uri:

          DATABASE_URI = 'postgresql://USER:PASSWORD@localhost:5432/DB'
 
      or set Flask enviroment variable: 
      
          Linux
            export SQLALCHEMY_DATABASE_URI = 'postgresql://USER:PASSWORD@localhost:5432/DB'  
      
          Windows
            $env:SQLALCHEMY_DATABASE_URI = 'postgresql://USER:PASSWORD@localhost:5432/DB'

  6. Create tables in DB

    python3 db_init.py
  
Run
------------

In your virtual env type:

    flask run
  
Initializing test data
------------

Go to http://127.0.0.1:5000/t to initiate test records in the database 

  
Reset DB
------------
In your virtual env type:

    python3 db_init.py


Production mode
------------

Set environment variable in .flaskenv file:

    FLASK_ENV=production

