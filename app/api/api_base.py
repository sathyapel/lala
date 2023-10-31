from fastapi import APIRouter
from fastapi import APIRouter
from  app.api.v1 import route_stories
base_router = APIRouter()

base_router.include_router(route_stories.router,tags=["stories_create"])

