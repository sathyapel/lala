from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column,relationship
from sqlalchemy import String,ForeignKey,Integer

class Base(DeclarativeBase):
    pass

