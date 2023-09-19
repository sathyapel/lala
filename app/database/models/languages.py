from app.database.models.base_class import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column,relationship
from sqlalchemy import String,ForeignKey,Integer
from sqlalchemy import JSON
from sqlalchemy.dialects.mysql import LONGTEXT
class LanguageModel(Base):
    __tablename__="language_model"


    id =mapped_column(Integer,primary_key=True)
    name = mapped_column(String(100),nullable=False)
    code = mapped_column(String(50),nullable=False)
    status = mapped_column(Integer)
    stories = relationship("StoriesModel",back_populates="languages")

    