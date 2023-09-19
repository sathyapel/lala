from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from typing import Generator    
from app.backend.core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
print("Database URL is ",SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL,echo=True)


SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
def get_db() -> Generator:  
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

