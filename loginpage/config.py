import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Name of Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'wastegen2019@gmail.com'
    MAIL_PASSWORD = 'leadersofthefuture'
    FLASK_ADMIN_SWATCH = 'paper'
    FLASK_RUN_PORT = 8000
    CSRF_ENABLED = True



