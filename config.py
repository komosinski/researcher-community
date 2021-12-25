import os
from dotenv import load_dotenv
#TODO: Remove it in the future
from temporary_config import DATABASE_URI


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    #  TODO: Delete/Hide some default config values like KEYs in the future

    SQLALCHEMY_DATABASE_URI =   os.environ.get('SQLALCHEMY_DATABASE_URI') or DATABASE_URI
    SECRET_KEY =  os.environ.get('SECRET_KEY') or '88d74de749c87a6b38400d2c3e62e802'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or'03b1aa0ca4845cebeb350af4440c284c'
    SECURITY_ACCOUNT_RECOVERY_SALT =  os.environ.get('SECURITY_ACCOUNT_RECOVERY_SALT') or '3a442018f74a034d1b499a405640c6a7'
    SECURITY_CHANGE_EMAIL_SALT = os.environ.get('SECURITY_CHANGE_EMAIL_SALT') or '10d7ce9ce5be51a09e678dc08ec55827'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT= int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USERNAME= 'kappa.science.mail@gmail.com'
    MAIL_PASSWORD= 'mkocde.jek83fP62.JKL'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'kappa.science.mail@gmail.com'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 100 * 1000 * 1000)  # 100 MB
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or '6Ldr23IdAAAAAAdwsCoT1r6NIpdmpyzxOaafY8fP'
    RECAPTCHA_PRIVATE_KEY =  os.environ.get('RECAPTCHA_PRIVATE_KEY') or '6Ldr23IdAAAAAHcZdWkjR4IWLcr3qpp6_i-N_xeT'
    PROFILE_IMAGE_URL =  os.environ.get('PROFILE_IMAGE_URL') or '/static/res/profileImages/'

    # Mail Limit = ML
    # per day
    CONFIRM_REGISTRATION_ML =  int(os.environ.get('CONFIRM_REGISTRATION_ML') or 5)
    INVITE_USER_ML = int(os.environ.get('INVITE_USER_ML') or 3)
    # per month
    CHANGE_MAIL_ML = int(os.environ.get('CHANGE_MAIL_ML') or 3)

    # Limit = L
    # per day
    REQUEST_ENDORSEMENT_L = int(os.environ.get('REQUEST_ENDORSEMENT_L') or 3)
 
    ENDORSEMENT_THRESHOLD =  int(os.environ.get('ENDORSEMENT_THRESHOLD') or 2)
    
