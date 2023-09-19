import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
class Settings:
    PROJECT_NAME:str = "LalaAI"
    PROJECT_VERSION: str = "1.0.0"

    MYSQL_USER:str = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD:str = os.getenv('MYSQL_PASSWORD')
    MYSQL_SERVER:str = os.getenv('MYSQL_SERVER')
    MYSQL_PORT:str = os.getenv('MYSQL_PORT')
    MYSQL_DATABASE:str =os.getenv('MYSQL_DATABASE')
    DATABASE_URL:str = 'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_SERVER, MYSQL_PORT,MYSQL_DATABASE)

settings = Settings()

print("databaseUrl",settings.DATABASE_URL)