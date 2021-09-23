import os

class DevelopmentConfig:
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='sqlite:///hasp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

Config=DevelopmentConfig

