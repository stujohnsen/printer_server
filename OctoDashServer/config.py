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
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SERVER_NAME = '0.0.0.0:6286'

class ProductionConfig(Config):
    """
    Production configurations
    """
    SERVER_NAME = '0.0.0.0:6286'

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
