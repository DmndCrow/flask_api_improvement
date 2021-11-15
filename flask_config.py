import os
from pathlib import Path

from dotenv import load_dotenv
from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint


load_dotenv()
BASE_PATH = Path(__file__).resolve().parent


class DbConfig:
    NEO4J_HOST = os.getenv('NEO4J_HOST')
    NEO4J_PORT = os.getenv('NEO4J_PORT')
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

    NEO4J_URL = f'neo4j://{NEO4J_HOST}:{NEO4J_PORT}'


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = os.getenv('SECRET_KEY')
