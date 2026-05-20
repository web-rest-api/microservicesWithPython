# Infrastructure layer — raw database queries.
#
# Functions here take a SQLAlchemy Session and return ORM objects.
# This is the only layer allowed to write SQL / ORM queries.
#
# Rules:
# - No HTTP knowledge here (no Request, no HTTPException)
# - No business rules here (no password hashing, no validation logic)
# - Every function receives `db: Session` as its first argument
#
# This file should implement:
# - create_user(db, data, hashed_password) -> User
# - get_user(db, user_id) -> User | None
# - list_users(db, limit, offset) -> tuple[list[User], int]
#
# See the README for the full implementation.
from sqlalchemy.orm import Session
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


def search_games(db: Session, q: str):
    return db.query(Game).filter(Game.title.ilike(f"%{q}%")).all()