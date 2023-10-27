
from pydantic import BaseModel,Field,validator
from typing import Optional
from datetime import datetime

class Stories(BaseModel):
    id:int 
    title:str 
    description:Optional[str] 
    category :str
    language :int
    status_flag :str
    schedule :datetime = Field(default=datetime.utcnow)
    created_at :datetime = Field(default=datetime.utcnow)
    updated_at :datetime = Field(default=datetime.utcnow)
    deleted_at :datetime = Field(default=None)
    keyword_old:Optional[str]
    keyword :Optional[str]
    youtube_id :str
    description_1 :Optional[str]

    