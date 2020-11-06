import os


class BaseConfig:
    """ Base Configurations """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    """ Development Configurations """
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_DEV')


class UnitTestingConfig(BaseConfig):
    """ Testing Configurations """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = None


class IntegrationTestingConfig(BaseConfig):
    """ Testing Configurations """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_TEST')


class ProductionConfig(BaseConfig):
    """ Production Configurations """
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_PROD')

