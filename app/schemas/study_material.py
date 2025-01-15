from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class StudyMaterialBase(BaseModel):
    title: str
    content_type: str
    content: Optional[str] = None
    file_path: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty_level: Optional[float] = None
    estimated_time: Optional[int] = None

class StudyMaterialCreate(StudyMaterialBase):
    pass

class StudyMaterialUpdate(StudyMaterialBase):
    pass

class StudyMaterialResponse(StudyMaterialBase):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 