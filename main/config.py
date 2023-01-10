import os 
# from .instance.secret_keys import SECRET_KEY

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///DCG_db').replace('://', 'ql://', 1)

SECRET_KEY = os.environ.get('SECRET_KEY', 'super_secret_key')

DEBUG = False

if DEBUG:
    SQLALCHEMY_ECHO = True

    DEBUG_TB_INTERCEPT_REDIRECTS = True