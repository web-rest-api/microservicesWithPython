# Interface layer — HTTP endpoints.
#
# This file defines the FastAPI router and maps HTTP verbs + paths to
# service function calls. It is the only layer that knows about HTTP.
#
# Rules:
# - Never call repository functions directly — always go through service
# - Catch ValueError from the service layer and raise HTTPException instead
# - Use Depends(get_db) to inject the database session
#
# This file should expose:
# - POST   /v1/users/          -> create a user
# - GET    /v1/users/          -> list users (with limit/offset pagination)
# - GET    /v1/users/{user_id} -> get one user by ID (404 if not found)
#
# See the README for the full implementation.
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


@router.get("/search/", response_model=list[GameResponse])
def search_games(q: str, db: Session = Depends(get_db)):
    return service.search_games(db, q)