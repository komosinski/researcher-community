# Private sources of the researcher.community project.

Overview of the sources
-----------------------

TODO high-level description of what is where, what purpose, directories, modules, dependencies within sources

`config/config.py` - flask server and logic config parameters

`config/models_config.py` - DB models' strings lengths

`config/auto_endorse_config.py` - Regular expressions for auto-endoring users based on email

------------------

`open_science` - flask server module

 <br />

`open_science/user` - user module with routes definitions and forms

`open_science/tag` - tag module with routes definitions and forms

`open_science/review` - review module with routes definitions, forms and helper functions associated with selecting reviewers

`open_science/notification` - notification module with routes definitions and helpers to create notifiactions

`open_science/search` - search module with helpers to preapare search queries 

`open_science/schedule` - scheduler module with daily and mothly jobs

 <br />

`open_science/templates` - all .html files

`open_science/static` - server static files

 <br />

`open_science/extensions.py` - extensions used in project

`open_science/__init__.py` - file that creates app and registers extensions

`open_science/models.py` - database models definitions

`open_science/db_helper.py` - functions with database queries

`open_science/db_queries.py` - database triggers

`open_science/enums.py` - enums e.g. EmailTypeEnum

`open_science/emial.py` - functions to send emails

`open_science/tokens.py` - functions to create and confirm tokens used in emails

`open_science/routes.py` - all available enpoints

`open_science/routes_def.py` - basic routes definitions

`open_science/forms.py` - forms for basic routes

`open_science/test_data.py` - has functions to create data for tests

`open_science/admin.py` - customization of admin panel

`open_science/strings.py` - strings definitions

------------------

`text_processing` - text processing module

 <br />
 
`server_files/generated_files` - directory which contain files generated by text_processing module (dictionary, similarities_matrix and tfidf_matrix)

Linux setup
-----------

1. Install and configure PostgreSQL

        https://www.postgresql.org/download/
    
    You can use:

        $ sudo apt install postgresql postgresql-contrib

2. Install libpq

        $ sudo apt install libpq - dev
    
3. Install python

        $ sudo apt install python3
        $ sudo apt install python3-pip python3-virtualenv python3-dev
    
4. Install poppler 
  
        $ sudo apt install poppler-utils build-essential libpoppler-cpp-dev pkg-config
      
5. Move to main directory and create python virtual environment

        python3 -m virtualenv venv
  
6. Activate virtual environment

        $ source venv/bin/activate
  
7. Install requirements
  
        pip install -r requirements.txt
  
8. Install nltk packages
  
    Run Python interptreter 
     
        python3
     
    And type:
   
        import nltk
        [nltk.download(pkg) for pkg in ['punkt', 'stopwords', 'wordnet', 'omw-1.4']]
     
9. Setup configuration file   config/config.py (mainly ROOTDIR and DATABASE_URI)
      
10. Create tables in the database

        python3 db_init.py

11. Setting up minimal permissions for files and directories
  
   `chmod -R 400 .` <br />
   `chmod 600 open_science/static/articles` <br />
   `chmod 600 open_science/static/res` <br />
   `chmod 600 open_science/static/res/profileImages` <br />
   `chmod 600 server_files/generated_files` <br />



Windows setup
-------------

This project is using poppler library whose installation on windows is problematic. You can try using Build tools for Visual Studio and Anaconda but we recommend using WSL (Windows Subsystem for Linux) for the whole environment.
      
1. Install and configure PostgreSQL on your local machine
  
        https://www.postgresql.org/download/
  
2. Enable WSL in widows. Run Window’s Powershell as an administrator:
     
        Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
    
3. Install Ubuntu from Microsoft Store
  
        https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6#activetab=pivot:overviewtab

4. Open Ubuntu app, do the initial setup and run the following commands:
      
        sudo apt-get clean
        sudo apt-get update
        sudo apt-get upgrade
    
5. Go to project's main directory and run WSL in terminal:

        wsl

6. Go through the steps in described earlier installation for Linux starting with step 2.
 

  
Run
---

If running the flask server, on Linux in your virtual environment type:

        flask run
 
On Windows you can do the same, but remember to use WSL.


Initializing test data
----------------------

If you want to initiate test data, you must ensure that there are pdf files in the folder open_science/static/articles named from 1.pdf to 130.pdf.

If articles folder contains pdf files, go to http://127.0.0.1:5000/t to initiate test records in the database.


Reset database
--------------
In your virtual environment, type:

        python3 db_init.py


Production mode
---------------

Set environment variable in .flaskenv file:

        FLASK_ENV=production
        FLASK_DEBUG=0

