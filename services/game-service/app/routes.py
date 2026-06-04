from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas import GameCreate, GameResponse
from app import service

router = APIRouter(prefix="/v1/games", tags=["games"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=GameResponse)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    return service.create_game(db, game)

@router.get("", response_model=list[GameResponse])
def get_games(db: Session = Depends(get_db)):
    return service.get_games(db)

@router.get("/{game_id}", response_model=GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    return service.get_game_by_id(db, game_id)

@router.get("/search/")
def search_games(q: str, db: Session = Depends(get_db)):
    return service.search_games(db, q)