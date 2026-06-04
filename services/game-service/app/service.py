from sqlalchemy.orm import Session
from app import repository

def create_game(db: Session, game_data):
    return repository.create_game(db, game_data)

def get_games(db: Session):
    return repository.get_games(db)

def get_game_by_id(db: Session, game_id: int):
    return repository.get_game_by_id(db, game_id)

def search_games(db: Session, query: str):
    return repository.search_games(db, query)