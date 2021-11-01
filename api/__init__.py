from flask import Flask
from dotenv import load_dotenv


load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('flask_config.Config')

    with app.app_context():
        from . import routes

        return app
