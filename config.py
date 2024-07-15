import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'development2024'
    ADMIN_EMAIL = 'biuro@addip.pl'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'data-dev2.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://DB_USER:#DB_USER_PASSWORD@localhost/flask_db'
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping' : True,}
    MAIL_SERVER = #server_address
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = #UserName
    MAIL_PASSWORD = #Password
    MAIL_DEBUGH = True


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://DB_USER:#DB_USER_PASSWORD@db/flask_db'
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping' : True,}
    MAIL_SERVER = #server_address
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = #UserName
    MAIL_PASSWORD = #Password
    MAIL_DEBUGH = True

config = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}
