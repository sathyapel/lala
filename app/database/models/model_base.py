""" this files refers the base file of all models reside here there are many ways to 
create tables for sql we can use alembic for vesrsioning
how to create a project 
 models.py
 |
 |_ model_base.py -> contains all model list here at last the meta_data of which
                    meta_data of all database
  -----other model .py files -> all orm models reside here
                    
"""
from .base_class import Base
from .stories import StoriesModel
from .categories import CategoriesModel
from .languages import LanguageModel
meta_data = Base.metadata