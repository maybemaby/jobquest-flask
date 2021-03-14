"""Settings for test app"""
TESTING = True
ENV = "development"
SQLALCHEMY_DATABASE_URI = "sqlite://"
SECRET_KEY = "not-so-secret-tests"
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = False
