from fastapi import FastAPI
import os 
import joblib
import pandas as pd
from fastapi.middleware.wsgi import WSGIMiddleware
from .feature.data_cleaning import *
from .dashboard.dash import dashApp as dashboard
from .db.model import Base
from .db.sessions import engine
from .api.api_base import base_router
from .core.config import settings

Base.metadata.create_all(bind=engine)

import json

ROOT_PATH = os.getcwd()
print("starthere")

def change_path_to_saved_models():
    if not(os.getcwd().__contains__("saved_model")):
            cur_dir=settings.ROOT_PATH
            app_dir_path = os.path.join(cur_dir,"app")
            os.chdir(app_dir_path)
            init_data_path=os.path.join(os.getcwd(),"saved_model")
            os.chdir(init_data_path)


change_path_to_saved_models()    
cat_and_lsa_df = pd.read_csv("content.csv")
lsa_trained = joblib.load('trained.pkl')

def include_router(app):   
	app.include_router(base_router)


app = FastAPI(title="LalaAI")

app.mount(path="/analytics", app=WSGIMiddleware(dashboard.server))
app.include_router(base_router)




@app.get("/refresh")
async def testApi(watching_video:str):
    """ check and refresh the categories from original database currently for inital testing
     it loads data from csv files  """
    try:
        
        stories_id_list=get_content_based_lsa(watching_video,15,lsa_trained,cat_and_lsa_df.copy())
        fil_stories=filter_by_lanaguage(stories_id_list,cat_and_lsa_df,None)[["id","title"]]
        content_list_tuples =list(fil_stories.itertuples(index=None,name=None))
        storiesids = reorder_list(content_list_tuples,watching_video)
        ids = [ids.get('s_id') for ids in storiesids ]
        final_df=cat_and_lsa_df.loc[cat_and_lsa_df["id"].isin(ids)]
        final_df = final_df[["id","title","image_link","duration",]].rename(columns={"image_link":"image"})
        final_df["title"] = final_df["title"].apply(lambda x: x.encode("utf8"))
        return final_df.to_dict(orient='records')
    except:
        return {"ErrorCode":1 ,"Data":None,"Message":"Invalid video title or video not found"}
      
    



@app.get("/")
async def root():
  cwd = os.getcwd()
  print(cwd)
  return {"Welcome to Lala Analytics"}