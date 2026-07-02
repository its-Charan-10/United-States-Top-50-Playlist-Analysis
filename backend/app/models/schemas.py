from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ContentBase(BaseModel):
    title: str
    description: str
    genre: List[str]
    thumbnailUrl: str
    backdropUrl: str
    videoUrl: str
    duration: str
    releaseYear: int
    type: str  # 'movie' or 'series'
    rating: float

class Content(ContentBase):
    id: str

class UserProfile(BaseModel):
    uid: str
    email: str
    displayName: Optional[str] = None
    photoURL: Optional[str] = None
    plan: str = "free" # free, basic, standard, premium
    watchlist: List[str] = []
