import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'THISSHOULDBEKEPTSECRET'
    SQLALCHEMY_DATABASE_URI = "postgres://abhqmfcmupjdte:9a29eaa024f3bc11ac8efaf1f59be6d901faffd5d3a0abe5d3cf9802e8c9108e@ec2-52-6-143-153.compute-1.amazonaws.com:5432/d9ma6ekrd6qc0d"

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'libmgmtstm@gmail.com'
    MAIL_PASSWORD = 'python-flask'
    ADMIN_USERNAME = 'ADMIN_USERNAME'
    ADMIN_PASSWORD = 'ADMIN_PASSWORD'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
