from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter

from app.schemas.stories import Stories
from app.db.sessions import get_db
from app.db.repo import handle_stories


router = APIRouter()

@router.post("/stories/create/")
def create_stories(stories:Stories,session:Session=Depends(get_db)):
    story = handle_stories.create_stories(stories,session)
    return story.json()