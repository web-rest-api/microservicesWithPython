from pydantic import BaseModel

class GameCreate(BaseModel):
    title: str
    genre: str
    platform: str
    cover_url: str

class GameResponse(GameCreate):
    id: int

    class Config:
        from_attributes = True