import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):

    #  TODO: Delete/Hide some default config values like KEYs in the future

    SERVER_NAME = os.environ.get('SERVER_NAME') or '127.0.0.1:5000'

    # 'postgresql://USER:PASSWORD@localhost:5432/DB_NAME'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or "postgresql://postgres:postgres@localhost:5432/open_science"
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

    START_SCHEDULER = True

    MAINTENANCE_MODE = False

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
    PAPER_L = int(os.environ.get('PAPER_L') or 10)

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

    # the maximum number of reviews a user can request
    MAX_CONFIDECNE_LEVEL = int(os.environ.get(
        'MAX_CONFIDECNE_LEVEL') or 3)

    # project directory path
    ROOTDIR = "./"

    #  to processing text dictionary
    DICTIONARY_FILE_PATH = 'generated/dictionary'

    # Path to processing text tfidf matrix mapping array
    TFIDF_MATRIX_MAPPING_ARRAY_FILE_PATH = 'generated/tfidf_matrix_mapping.npy'

    # Path to processing text tfidf matrix
    TFIDF_MATRIX_FILE_PATH = 'generated/tfidf_matrix'

    # Path to processing text similarities matrix mapping array
    SIMILARITIES_MATRIX_MAPPING_ARRAY_FILE_PATH = 'generated/similarities_matrix_mapping.npy'

    # Path to processing text similarities matrix
    SIMILARITIES_MATRIX_FILE_PATH = 'generated/similarities_matrix.npy'

    # Path to processing text users plot
    USERS_PLOT_2D_FILE_PATH = 'open_science/static/res/users_plot'

    USERS_PLOT_3D_FILE_PATH = 'open_science/templates/users_plot_3D.html'

    # Path to pdfs folder
    PDFS_DIR_PATH = 'open_science/static/articles'

    # Path of profile pics directory
    PROFILE_IMAGES_DIR_PATH = 'open_science/static/res/profileImages'

    # only for tests
    # using ./open_science/static/articles/1.pdf causes bad request: GET /paper/1/open_science/static/articles/1.pdf
    # using /static/articles/1.pdf causes correct request: GET /static/articles/1.pdf
    # it is working the same way as for styles and resources
    TEST_PDFS_DIR_PATH = '/static/articles/'
