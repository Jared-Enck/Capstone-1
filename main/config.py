import os
from .instance import secret_keys

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///DCG_db').replace('://', 'ql://', 1)

SECRET_KEY_VAL = os.environ.get('SECRET_KEY', secret_keys.SECRET_KEY)

DEBUG = False

SQLALCHEMY_ECHO = False

DEBUG_TB_INTERCEPT_REDIRECTS = True