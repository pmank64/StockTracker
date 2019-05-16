from flask import Flask
from app.config import Config
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app import routes