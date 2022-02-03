# Private sources of the openscience project.

Introduction
------------

Linux setup
------------

  1. Install and configure PostgreSQL on your local machine

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
     
  
  9. (Temporary step*) Create config_db.py file in config/ directory which must contain database uri to your DB.

          DATABASE_URI = 'postgresql://USER:PASSWORD@localhost:5432/open_science'
 
      or set Flask enviroment variable: 
     
          export SQLALCHEMY_DATABASE_URI = 'postgresql://USER:PASSWORD@localhost:5432/open_science'  
      
  10. Create tables in 

    python3 db_init.py


Windows setup
------------

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
------------

On Linux in your virtual environment type:

    flask run
 
On Windows you must do the same but remember to using WSL.
 
Initializing test data
------------

If you want to initiate test data, you must ensure that there are pdf files in the folder open_science/static/articles named from 1.pdf to 130.pdf.

If articles folder contains pdf files, go to http://127.0.0.1:5000/t to initiate test records in the database.


Reset DB
------------
In your virtual environment type:

    python3 db_init.py


Production mode
------------

Set environment variable in .flaskenv file:

    FLASK_ENV=production
    FLASK_DEBUG=0

