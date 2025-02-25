from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import json
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_ignore_empty=True)

    BOT_TOKEN: str
    API_HASH: str = 'b18441a1ff607e10a989891a5462e627'
    API_ID: int = 2040

    SESSION_NAME: str = 'bot'
    SUPPORT: str = '@support'
    OWNER: int = 0
    
    BOT_USERNAME: str = 'usernamebot'
    BOT_CHANNEL: str = 'username'

    ACTIVE_REDIS: bool = False
    DB_ENGINE: str = 'sqlite3'
    DB_NAME: str = 'mydatabase'
    DB_HOST: str = 'localhost'
    DB_USER: str = 'root'
    DB_PORT: int = 3306
    DB_PASSWORD: str = 'root'


BASE_DIR = Path(os.path.dirname(__file__)).parent.parent
TEXTS = json.load(open(BASE_DIR / 'src/utils/texts.json', 'r', encoding='utf-8'))
SETTINGS = Settings()
