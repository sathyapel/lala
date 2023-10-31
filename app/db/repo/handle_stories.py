from app.db.model import StoriesModel
from app.schemas.stories import Stories
from sqlalchemy.orm import Session

def create_stories(stories:Stories,db:Session):
    story = StoriesModel(
        title=stories.title,
        description=stories.description,
        category=stories.category,
        language=stories.language,
        status_flag=stories.status_flag,
        schedule=stories.schedule,
        created_at =stories.created_at,
        updated_at=stories.updated_at,
        deleted_at = stories.deleted_at,
        keyword_old=stories.keyword_old,
        keyword=stories.keyword_old,
        youtube_id=stories.youtube_id,
        description_1=stories.description_1 )
    
    db.add(story)
    db.commit()
    db.refresh(story)
    return story
    