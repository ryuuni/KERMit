import os


class BaseConfig:
    """ Base Configurations """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ERROR_MESSAGE_KEY = 'message'


class DevelopmentConfig(BaseConfig):
    """ Development Configurations """
    ENV = 'development'
    DEBUG = True
    BCRYPT_SALT_ROUNDS = 5
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_DEV')


class UnitTestingConfig(BaseConfig):
    """ Testing Configurations """
    DEBUG = True
    BCRYPT_SALT_ROUNDS = 1
    SQLALCHEMY_DATABASE_URI = None


class IntegrationTestingConfig(BaseConfig):
    """ Testing Configurations """
    DEBUG = True
    BCRYPT_SALT_ROUNDS = 5
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_TEST')


class ProductionConfig(BaseConfig):
    """ Production Configurations """
    DEBUG = False
    ENV = 'production'
    BCRYPT_SALT_ROUNDS = 10
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_PROD')

