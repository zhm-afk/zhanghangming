import os
from datetime import timedelta
import urllib.parse

basedir = os.path.abspath(os.path.dirname(__file__))
password = urllib.parse.quote('Ailing@200930')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key_change_in_production')
    DEBUG = False
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_dev_key_change_in_production')
    # 设置token有效期为30天
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ERROR_MESSAGE_KEY = 'message'
    
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI服务API密钥
    AI_API_KEY = os.getenv('AI_API_KEY', '')

class DevelopmentConfig(Config):
    DEBUG = True
    # MySQL开发环境连接
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URL', 
        f'mysql+pymysql://root:{password}@localhost/smart_band'
    )

class ProductionConfig(Config):
    DEBUG = False
    # MySQL生产环境连接
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        f'mysql+pymysql://root:{password}@localhost/smart_band'
    )

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}