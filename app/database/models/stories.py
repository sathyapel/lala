from app.database.models.base_class import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column,relationship
from sqlalchemy import String,ForeignKey,Integer
from sqlalchemy import JSON
from sqlalchemy.dialects.mysql import LONGTEXT
class StoriesModel(Base):
    __tablename__= "stories_model"

    
    id = mapped_column(Integer,primary_key=True)
    title = mapped_column(String(255),nullable=True)
    duration = mapped_column(String(20))
    category = mapped_column(JSON)
    language = mapped_column(Integer,ForeignKey("language_model.id"))
    status_flag = mapped_column(Integer)
    keyword = mapped_column(JSON,nullable=True)
    description_1 = mapped_column(LONGTEXT)
    keyword_str = mapped_column(LONGTEXT)
    cat_category = mapped_column(LONGTEXT)
    categories_str=mapped_column(LONGTEXT)
    cat_formated = mapped_column(LONGTEXT)
    description_lsa = mapped_column(LONGTEXT)
    content = mapped_column(LONGTEXT)

    languages =relationship("LanguageModel",back_populates="stories")
    
    
    
   
    




