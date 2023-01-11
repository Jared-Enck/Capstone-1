import os
 
try:
    from .instance.secret_keys import SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
except:
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    
try:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///DCG_db')
except:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///DCG_db').replace('://', 'ql://', 1)

SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = False

if DEBUG:    
    
    SQLALCHEMY_ECHO = True

    DEBUG_TB_INTERCEPT_REDIRECTS = True
    