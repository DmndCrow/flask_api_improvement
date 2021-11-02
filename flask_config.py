import os

from dotenv import load_dotenv

load_dotenv()


class DbConfig:
    database = ''
    user = ''
    password = ''
    host = ''
    SQLALCHEMY_DATABASE_URI = 'sqlite:////db/base.db'
    SQLALCHEMY_BINDS = {
        'elastic': 'sqlite:////db/elastic.db',
        'neo4j': 'sqlite:////db/neo4j.db'
    }
 

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = os.getenv('SECRET_KEY')
