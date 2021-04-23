import os


class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL")
    MAIL_PASSWORD = os.environ.get("MAIL_PS")
    MAIL_DEFAULT_SENDER = ("Flasbklog1 Admin", "noreply@flaskblog1.com")
