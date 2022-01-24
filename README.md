# Private sources of the openscience project.

Introduction
------------


Linux setup
------------

  1. Install and configure PostgreSQL on your local machine

    https://www.postgresql.org/download/
    
  2. Install poppler 
  
    $ sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev
      
  3. Move to main directory and create python virtual environment

    python3 -m virtualenv venv
  
  4. Activate virtual environment

    $ source venv/bin/activate
  
  5. Install requirements
  
    pip install -r requirements.txt
  
  6. Install nltk packages
  
   Run Python interptreter 
     
    python3
     
   And type:
   
    import nltk
    [nltk.download(pkg) for pkg in ['punkt', 'stopwords', 'wordnet', 'omw-1.4']]
     
  
  7. (Temporary step*) Create temporary_config.py file in main directory which must contain database uri to your DB. Defualt DB_NAME is postgres.

          DATABASE_URI = 'postgresql://USER:PASSWORD@localhost:5432/open_science'
 
      or set Flask enviroment variable: 
     
          export SQLALCHEMY_DATABASE_URI = 'postgresql://USER:PASSWORD@localhost:5432/open_science'  
      
  8. Create tables in DB

    python3 db_init.py


Windows setup
------------

This project is using poppler library whose installation on windows is very problematic. You can try using Build tools for Visual Studio and Anaconda but we recommend using WSL (Windows Subsystem for Linux) for the whole environment.
      
  1. Install and configure PostgreSQL on your local machine
  
    https://www.postgresql.org/download/
  
  2. Enable WSL in widows. Run Window’s Powershell as an administrator:
     
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
    
  3. Install Ubuntu from Microsoft Store
  
    https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6#activetab=pivot:overviewtab

  4. Open Ubuntu app and do the initial setup and then run the following commands:
      
    sudo apt-get clean
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt install python3 poppler-utils python3-pip python3.8-venv -y
    sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev -y
    sudo apt install libpq-dev python3-virtualenv -y
    
  5. Go to project's main directory and run WSL in terminal:

    wsl

  6. Create python virtual env

    python3 -m virtualenv venv
 
  7. Activate virtual env
 
    source venv/bin/activate
      
  8. Install requirements

    pip install -r requirements.txt
 
  9. Install nltk packages
  
   Run Python interptreter 
     
    python3
     
   And type:
   
    import nltk
    [nltk.download(pkg) for pkg in ['punkt', 'stopwords', 'wordnet', 'omw-1.4']]
 
  10. Temporary step*) Create temporary_config.py file in main directory which must contain database uri to your DB. Defualt DB_NAME is postgres.

    DATABASE_URI = 'postgresql://USER:PASSWORD@localhost:5432/open_science'
 
   or set Flask enviroment variable: 
      
    export SQLALCHEMY_DATABASE_URI = 'postgresql://USER:PASSWORD@localhost:5432/open_science'  
            
  11. Create tables in DB

    python3 db_init.py

  
  
Run
------------

On Linux in your virtual environment type:

    flask run
 
On Windows you must do the same but remember to using WSL.
 
Initializing test data
------------

Go to http://127.0.0.1:5000/t to initiate test records in the database 

  
Reset DB
------------
In your virtual environment type:

    python3 db_init.py


Production mode
------------

Set environment variable in .flaskenv file:

    FLASK_ENV=production

