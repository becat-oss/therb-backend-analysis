import os

class DevelopmentConfig:
    DEBUG=True
    #SQLALCHEMY_DATABASE_URI='sqlite:///heatload.db'
    #SQLALCHEMY_DATABASE_URI='sqlite:///graphql.db'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}/{name}'.format(**{
        'user': 'therbuser',
        'password': 'therb',
        'host': '127.0.0.1:54321',
        'name': 'project'
    })
    #SQLALCHEMY_DATABASE_URI = "postgresql://therbuser:therb@localhost:54321"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

Config=DevelopmentConfig

