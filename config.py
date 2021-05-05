import os
basedir = os.path.abspath(os.path.dirname(__file__))

#str ="jdbc:postgresql:User=postgres;Password=1234;Database=postgres;server=localhost;Port=5432;"
#DATABASE_URL=str



CONFIG = {
   'postgresUrl':'localhost:5432',
   'postgresUser':'postgres',
   'postgresPass':'1234',
   'postgresDb':'postgres',
}

POSTGRES_URL = CONFIG['postgresUrl']
POSTGRES_USER = CONFIG['postgresUser']
POSTGRES_PASS = CONFIG['postgresPass']
POSTGRES_DB = CONFIG['postgresDb']
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PASS, url=POSTGRES_URL, db=POSTGRES_DB)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = DB_URL


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True