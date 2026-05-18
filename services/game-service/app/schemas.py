from pydantic import BaseModel
from datetime import datetime

class GameCreate(BaseModel):
    title: str
    genre: str
    description: str

class GameOut(BaseModel):
    id: str
    title: str
    genre: str
    description: str | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class GameList(BaseModel):
    items: list[GameOut]
    total: int
    limit: int
    offset: int