import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    ROOT_PATH = os.getcwd()
    PROJECT_NAME:str = "LALA AI"
    PROJECT_VERSION: str = "1.0.0"

    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER : str = os.getenv("MYSQL_SERVER","localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT",3306) # default postgres port is 5432
    MYSQL_DATABASE : str = os.getenv("MYSQL_DATABASE","apilala")
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DATABASE}"

settings = Settings()