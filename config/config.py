import os
from dotenv import load_dotenv
# TODO: Remove it in the future
try:
    from config.config_db import DATABASE_URI
except ImportError or ModuleNotFoundError:
    DATABASE_URI = None
    print('If you have not set an environment variable\
         SQLALCHEMY_DATABASE_URI , set it')

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    #  TODO: Delete/Hide some default config values like KEYs in the future

    SERVER_NAME = os.environ.get('SERVER_NAME') or '127.0.0.1:5000'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or DATABASE_URI
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or '88d74de749c87a6b38400d2c3e62e802'
    SECURITY_PASSWORD_SALT = os.environ.get(
        'SECURITY_PASSWORD_SALT') or '03b1aa0ca4845cebeb350af4440c284c'
    SECURITY_ACCOUNT_RECOVERY_SALT = os.environ.get(
        'SECURITY_ACCOUNT_RECOVERY_SALT') or '3a442018f74a034d1b499a405640c6a7'
    SECURITY_CHANGE_EMAIL_SALT = os.environ.get(
        'SECURITY_CHANGE_EMAIL_SALT') or '10d7ce9ce5be51a09e678dc08ec55827'
    SECURITY_PROFILE_DELETE_SALT = os.environ.get(
        'SECURITY_PROFILE_DELETE_SALT') or '5381ce88896f17316c40d7dcb8d6acbc'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USERNAME = 'kappa.science.mail@gmail.com'
    MAIL_PASSWORD = 'mkocde.jek83fP62.JKL'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = os.environ.get(
        'MAIL_DEFAULT_SENDER') or 'kappa.science.mail@gmail.com'
    MAX_CONTENT_LENGTH = int(os.environ.get(
        'MAX_CONTENT_LENGTH') or 100 * 1000 * 1000)  # 100 MB
    RECAPTCHA_PUBLIC_KEY = os.environ.get(
        'RECAPTCHA_PUBLIC_KEY') or '6Ldr23IdAAAAAAdwsCoT1r6NIpdmpyzxOaafY8fP'
    RECAPTCHA_PRIVATE_KEY = os.environ.get(
        'RECAPTCHA_PRIVATE_KEY') or '6Ldr23IdAAAAAHcZdWkjR4IWLcr3qpp6_i-N_xeT'

    # Mail Limit = ML
    # per day
    CONFIRM_REGISTRATION_ML = int(
        os.environ.get('CONFIRM_REGISTRATION_ML') or 5)
    INVITE_USER_ML = int(os.environ.get('INVITE_USER_ML') or 3)
    # per month
    CHANGE_MAIL_ML = int(os.environ.get('CHANGE_MAIL_ML') or 3)

    # Limit = L
    # per day
    REQUEST_ENDORSEMENT_L = int(os.environ.get('REQUEST_ENDORSEMENT_L') or 3)

    ENDORSEMENT_THRESHOLD = int(os.environ.get('ENDORSEMENT_THRESHOLD') or 2)

    # Submit comments per day
    COMMENT_L = int(os.environ.get('COMMENT_L') or 500)

    # Upload papers per day
    PAPER_L = int(os.environ.get('PAPER_L') or 100)

    # Create tags per day
    TAGS_L = int(os.environ.get('TAGS_L') or 100)

    # Number of days to the end of the assumed review writing time
    REVIEW_DEADLINE_REMIND = int(os.environ.get('REVIEW_DEADLINE_REMIND') or 2)

    # Number of red flags required to hide item
    RED_FLAGS_THRESHOLD = int(os.environ.get('RED_FLAGS_THRESHOLD') or 5)

    # Exclusion of a reviewer
    # who is a co-author of papers by all authors of the reviewed paper
    EXCLUDE_CO_AUTHOR_FOR_REVIEW_DAYS = int(os.environ.get(
        'EXCLUDE_CO_AUTHOR_FOR_REVIEW_DAYS') or 730)

    # Exclusion of a reviewer
    # for whom the current authors reviewed any paper
    # within the last n-days
    EXCLUDE_REVIEWED_AUTHOR_FOR_REVIEW_DAYS = int(os.environ.get(
        'EXCLUDE_REVIEWED_AUTHOR_FOR_REVIEW_DAYS') or 730)

    # if user declined review request with respond “Don’t have time”
    # don’t ask him for review request to this paper fot N days.
    EXCLUDE_DECLINED_REQUEST_TIME_DAYS = int(os.environ.get(
        'EXCLUDE_REVIEWED_AUTHOR_FOR_REVIEW_DAYS') or 14)

    # To calculate workload of researchers
    # how many reviews they agreed to prepare in the last period of time
    REVIEWER_WORKOLOAD_ON_DAYS = int(os.environ.get(
        'REVIEWER_WORKOLOAD_ON_DAYS') or 365)

    # Url to processing text dictionary
    DICTIONARY_URL = './server_files/generated_files/dictionary'

    # Url to processing text tfidf matrix
    TFIDF_MATRIX_URL = './server_files/generated_files/tfidf_matrix'

    # Url to processing text similarities matrix
    SIMILARITIES_MATRIX_URL = \
        './server_files/generated_files/similarities_matrix.npy'
    # Url to processing text users plot
    USERS_PLOT_URL = './open_science/static/res/users_plot'

    # the maximum number of reviews a user can request
    MAX_CONFIDECNE_LEVEL = int(os.environ.get(
        'MAX_CONFIDECNE_LEVEL') or 3)

    # Url to pdfs folder
    PDFS_FOLDER_URL = '/static/articles/'

    # Full url to pdfs folder
    PDFS_FOLDER_FULL_URL = 'open_science/static/articles/'

    # project directory path
    ROOTDIR = "/home/marek/studia/inżynierka4"
    
    # url of profile pics directory
    PROFILE_IMAGE_URL = os.environ.get(
        'PROFILE_IMAGE_URL') or '/static/res/profileImages/'
