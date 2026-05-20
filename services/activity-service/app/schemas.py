from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GameOut(BaseModel):
    id: str
    title: str
    genre: str
    description: Optional[str] = None

class ActivityCreate(BaseModel):
    user_id: str
    game_id: str
    action: str
    duration_minutes: Optional[int] = None

class ActivityOut(BaseModel):
    id: str
    user_id: str
    action: str
    duration_minutes: Optional[int]
    created_at: datetime
    game: Optional[GameOut] = None

    model_config = {"from_attributes": True}

class ActivityList(BaseModel):
    items: list[ActivityOut]
    total: int
    limit: int
    offset: int