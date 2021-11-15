from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from . import utils

load_dotenv()
db = SQLAlchemy()

from . import db_connection


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('flask_config.DbConfig')
    app.config.from_object('flask_config.Config')
    
    db.init_app(app)

    with app.app_context():
        from api.routes.utils import utils_bp
        from api.routes.person import person_bp
        from api.routes.organization import organization_bp
        from api.routes.membership import membership_bp

        app.register_blueprint(utils_bp)
        app.register_blueprint(person_bp, url_prefix='/api/person')
        app.register_blueprint(organization_bp, url_prefix='/api/organization')
        app.register_blueprint(membership_bp, url_prefix='/api/membership')

        return app
