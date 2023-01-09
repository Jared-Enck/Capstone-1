import os, sys, inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))

if cmd_folder not in sys.path:
     sys.path.insert(0, cmd_folder)
     
from .instance.secret_keys import SECRET_KEY

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///DCG_db').replace('://', 'ql://', 1)

SECRET_KEY_VAL = os.environ.get('SECRET_KEY', SECRET_KEY)

DEBUG = False

SQLALCHEMY_ECHO = False

DEBUG_TB_INTERCEPT_REDIRECTS = True