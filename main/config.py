import os
 
DEBUG = False

try:
    from .instance.secret_keys import SECRET_KEY
except:
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    
SECRET_KEY = os.environ.get('SECRET_KEY', f'{SECRET_KEY}')
    
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///DCG_db').replace('://', 'ql://', 1)

if DEBUG:
    SQLALCHEMY_ECHO = True

    DEBUG_TB_INTERCEPT_REDIRECTS = True
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///DCG_db')

SQLALCHEMY_TRACK_MODIFICATIONS = False