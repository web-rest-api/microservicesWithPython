from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Game

def create_game(db: Session, game_data):
    game = Game(**game_data.dict())
    db.add(game)
    db.commit()
    db.refresh(game)
    return game

def get_games(db: Session):
    return db.query(Game).all()

def get_game_by_id(db: Session, game_id: int):
    return db.query(Game).filter(Game.id == game_id).first()

def search_games(db: Session, query: str):
    return db.query(Game).filter(
        Game.title.ilike(f"%{query}%")
    ).all()