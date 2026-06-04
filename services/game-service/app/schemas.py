from pydantic import BaseModel


class GameCreate(BaseModel):
    title: str
    genre: str
    platform: str
    cover_url: str


class GameOut(BaseModel):
    id: str
    title: str
    genre: str
    platform: str
    cover_url: str

    model_config = {"from_attributes": True}


class GameList(BaseModel):
    items: list[GameOut]
    total: int
    limit: int
    offset: int