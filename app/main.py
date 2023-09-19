from fastapi import FastAPI
import os 
from app.database.models.base_class import Base as BaseMeta
from app.database.session import engine 
from app.backend.core.config import settings
from app.database.models.model_base import meta_data
from fastapi import Depends
from app.database.session import get_db
from sqlalchemy.orm import Session
from .database.models.categories import CategoriesModel
import pandas as pd
import joblib
from .feature.data_cleaning import *

import json
meta_data.create_all(bind=engine)
if not(os.getcwd().__contains__("saved_model")):
          cur_dir = os.getcwd()
          app_dir_path = os.path.join(cur_dir,"app")
          os.chdir(app_dir_path)
          init_data_path=os.path.join(os.getcwd(),"saved_model")
          os.chdir(init_data_path)
cat_and_lsa_df = pd.read_csv("content.csv")
lsa_trained = joblib.load('trained.pkl')
    
app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)



@app.get("/refresh")
async def testApi(watching_video:str,dbSession:Session =Depends(get_db)):
    """ check and refresh the categories from original database currently for inital testing
     it loads data from csv files  """
    try:
        
        stories_id_list=get_content_based_lsa(watching_video,15,lsa_trained,cat_and_lsa_df.copy())
        fil_stories=filter_by_lanaguage(stories_id_list,cat_and_lsa_df,None)[["id","title"]]
        content_list_tuples =list(fil_stories.itertuples(index=None,name=None))
        storiesids = reorder_list(content_list_tuples,watching_video)
        ids = [ids.get('s_id') for ids in storiesids ]
        final_df=cat_and_lsa_df.loc[cat_and_lsa_df["id"].isin(ids)]
        return final_df[["id","title","image_link","duration",]].to_dict(orient='records')
    except:
        return {"ErrorCode":1 ,"Data":None,"Message":"Invalid video title or video not found"}
      
    



@app.get("/")
async def root():
  cwd = os.getcwd()
  print(cwd)
  return {"Welcome to Lala Analytics"}