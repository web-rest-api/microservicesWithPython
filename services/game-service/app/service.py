# Application layer — business logic.
#
# This is where decisions live: hashing passwords, raising errors when a user
# is not found, converting ORM objects into Pydantic schemas before returning.
#
# Rules:
# - Only calls repository functions — never queries the DB directly
# - Returns Pydantic schemas (UserOut, UserList), not raw ORM objects
# - Raises ValueError for business errors (routes.py turns them into HTTP errors)
#
# This file should implement:
# - add_user(db, data) -> UserOut
# - fetch_user(db, user_id) -> UserOut   (raises ValueError if not found)
# - fetch_all_users(db, limit, offset) -> UserList
#
# Note: _hash_password is a placeholder for now — it will be replaced
# with passlib in Module 6.
#
# See the README for the full implementation.
from sqlalchemy.orm import Session
from app import repository
from app.schemas import GameCreate


def create_game(db: Session, game: GameCreate):
    return repository.create_game(db, game)


def get_games(db: Session):
    return repository.get_games(db)


def get_game_by_id(db: Session, game_id: int):
    return repository.get_game_by_id(db, game_id)


def search_games(db: Session, q: str):
    return repository.search_games(db, q)