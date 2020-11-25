"""
Configuration helper file, responsible for allowing specific Flask configurations
for different environments.
"""
# pylint: disable=too-few-public-methods
import os


class BaseConfig:
    """ Base Configurations """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CORS_HEADERS = 'Content-Type'


class DevelopmentConfig(BaseConfig):
    """ Development Configurations """
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_DEV')
    CORS_HEADERS = 'Content-Type'
    CORS_SUPPORTS_CREDENTIALS=True


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
    CORS_HEADERS = 'Content-Type'
