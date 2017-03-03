# config.py

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SERVER_NAME = 'localhost:6286'

class ProductionConfig(Config):
    """
    Production configurations
    """
    SERVER_NAME = 'localhost:6286'

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
