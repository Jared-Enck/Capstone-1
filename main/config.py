import os 
try:
    from .instance.secret_keys import SECRET_KEY
except:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super_secret_key')

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///DCG_db').replace('://', 'ql://', 1)

DEBUG = False

if DEBUG:
    SQLALCHEMY_ECHO = True

    DEBUG_TB_INTERCEPT_REDIRECTS = True