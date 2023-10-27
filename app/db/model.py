
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base






Base = declarative_base()
class StoriesModel(Base):
  
    __tablename__='stories'
    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String(1024),nullable=False,)
    description = Column(Text,nullable=False)
    category = Column(String(1024),nullable=False)
    language = Column(String(255))
    status_flag = Column(String(500))
    schedule = Column(DateTime())
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    keyword_old = Column(String(1024))
    keyword = Column(String(1024))
    youtube_id = Column(String(1024))
    description_1 = Column(Text)
    

class CategoriesModel(Base):
  
  ##id,name,thum_pic,status_flag,language,create_at,update_at,deleted_at
    __tablename__="categories"


    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String(1024),nullable=False)
    language = Column(Integer,ForeignKey("languages.id"),nullable=False) 
    status_flag = Column(Integer,nullable=False)
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
    deleted_at = Column(DateTime)
    of_language = relationship("LanguageModel",back_populates="in_lanugage")


class LanguageModel(Base):
    
   ##id,name,status,code,deleted_at
   __tablename__ = "languages"


   id = Column(Integer,primary_key=True)
   name = Column(String(255),nullable=False)
   status = Column(Integer,nullable=False,default=1)
   lang_code = Column(String(40),nullable=True)
   deleted_at = Column(DateTime)
   in_language = relationship("CategoriesModel",back_populates="of_language")


  



