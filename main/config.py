import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','postgresql:///DCG_db').replace("://", "ql://", 1)

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_ECHO = False

SECRET_KEY = os.environ.get('SECRET_KEY','3f44cd49d69e821aa140f13a49f432b073e311a264583ab7ed4340b714da0db8')

DEBUG_TB_INTERCEPT_REDIRECTS = False

DEBUG = False