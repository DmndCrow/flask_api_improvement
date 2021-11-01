import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = os.getenv('SECRET_KEY')
