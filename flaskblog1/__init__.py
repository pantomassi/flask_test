import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config["SECRET_KEY"] = "958e97ae1c05f9b41ae8f1dc52e44e43"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PS")
app.config["MAIL_DEFAULT_SENDER"] = (
    "Flasbklog1 Admin", "noreply@flaskblog1.com")
mail = Mail(app)


from flaskblog1 import routes
