import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Name of Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    # FLASK_ADMIN_SWATCH = os.environ.get('ADMIN_SWATCH')
    FLASK_ADMIN_SWATCH = 'paper'
    FLASK_RUN_PORT = 8000
    CSRF_ENABLED = True
    # SECURITY_PASSWORD_HASH= 'pbkdf2_sha512'
    # SECURITY_PASSWORD_SALT = '123456'


