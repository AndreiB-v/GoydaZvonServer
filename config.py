"""Flask config."""
from os import environ, path

from dotenv import load_dotenv

load_dotenv() # Импортируем и используем функцию для автоматического считывания значений из файла .env
base_dir = path.abspath(path.dirname(__file__))


class Config:
    SECRET_KEY = environ.get("SECRET_KEY") or "never_gues_my_key"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

