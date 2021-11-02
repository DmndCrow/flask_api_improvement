from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from . import utils

load_dotenv()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('flask_config.DbConfig')
    app.config.from_object('flask_config.Config')
    
    db.init_app(app)

    with app.app_context():
        from . import routes

        return app
