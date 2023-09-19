from app.database.models.base_class import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column,relationship
from sqlalchemy import String,ForeignKey,Integer

class CategoriesModel(Base):
    __tablename__ = "categories_model"

   
    id = mapped_column(Integer,primary_key=True)
    name = mapped_column(String(255))
    status_flag = mapped_column(Integer,nullable=False)
    language = mapped_column(Integer,nullable=False)
      