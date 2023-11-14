
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped,registry
import sqlalchemy.orm as sa


mapper_registry = registry()


class Base(DeclarativeBase):
    pass

class StoriesModel(Base):
  
    __tablename__='stories'
    id:Mapped[int] = sa.mapped_column(Integer, primary_key=True,nullable=False)
    title:Mapped[str] = sa.mapped_column(String(1024),nullable=False,)
    description:Mapped[str] = sa.mapped_column(Text,nullable=False)
    category:Mapped[str] = sa.mapped_column(String(1024),nullable=False)
    language:Mapped[str] = sa.mapped_column(String(255))
    status_flag:Mapped[str] = sa.mapped_column(String(500))
    schedule:Mapped[DateTime] = sa.mapped_column(DateTime)
    created_at:Mapped[DateTime] = sa.mapped_column(DateTime,default=datetime.datetime.utcnow)
    updated_at:Mapped[DateTime] = sa.mapped_column(DateTime)
    deleted_at:Mapped[DateTime] = sa.mapped_column(DateTime)
    keyword_old:Mapped[str] = sa.mapped_column(String(1024))
    keyword:Mapped[str] = sa.mapped_column(String(1024))
    youtube_id:Mapped[str] = sa.mapped_column(String(1024))
    description_1:Mapped[str] = sa.mapped_column(Text)

class LanguageModel(Base):
    
   ''' `id`,`name`,`status`,`lang_code`,`deleted_at`'''
   __tablename__ = "languages"


   id:Mapped[int] = sa.mapped_column(Integer,primary_key=True)
   name:Mapped[str] = sa.mapped_column(String(255),nullable=False)
   status:Mapped[int] = sa.mapped_column(Integer,nullable=False,default=1)
   lang_code:Mapped[str] = sa.mapped_column(String(40),nullable=True)
   deleted_at:Mapped[DateTime] = sa.mapped_column(DateTime,nullable=True)
   lang_relation:Mapped["CategoriesModel"] = relationship(back_populates="cat_language")    

class CategoriesModel(Base):
  
  ##id,name,thum_pic,status_flag,language,create_at,update_at,deleted_at
    __tablename__="categories"


    id:Mapped[int] = sa.mapped_column(Integer,primary_key=True,nullable=False)
    name:Mapped[int] = sa.mapped_column(String(1024),nullable=False)
    language:Mapped[int]  = sa.mapped_column(Integer,ForeignKey("languages.id"),nullable=False) 
    status_flag:Mapped[int] = sa.mapped_column(Integer,nullable=False)
    created_at:Mapped[DateTime] = sa.mapped_column(DateTime,default=datetime.datetime.utcnow)
    deleted_at:Mapped[DateTime] = sa.mapped_column(DateTime,nullable=True)
    cat_language:Mapped["LanguageModel"] = relationship(back_populates="lang_relation")





   

  



