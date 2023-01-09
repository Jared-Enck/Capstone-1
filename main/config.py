import os
from .instance.secret_keys import SECRET_KEY

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///DCG_db').replace('://', 'ql://', 1)

SECRET_KEY_VAL = os.environ.get('SECRET_KEY', SECRET_KEY)

DEBUG = False

SQLALCHEMY_ECHO = False

DEBUG_TB_INTERCEPT_REDIRECTS = True