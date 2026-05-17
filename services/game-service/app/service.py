from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import GameCreate
import app.repository as repository

async def add_game(db: AsyncSession, game: GameCreate):
    return await repository.create_game(db, game)

async def list_games(db: AsyncSession):
    return await repository.get_games(db)

async def get_game(db: AsyncSession, game_id: int):
    return await repository.get_game_by_id(db, game_id)

async def search(db: AsyncSession, term: str):
    return await repository.search_games(db, term)