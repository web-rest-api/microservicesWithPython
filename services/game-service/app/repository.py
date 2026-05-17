from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Game
from app.schemas import GameCreate

async def create_game(db: AsyncSession, game: GameCreate):
    db_game = Game(**game.model_dump())
    db.add(db_game)
    await db.commit()
    await db.refresh(db_game)
    return db_game

async def get_games(db: AsyncSession):
    result = await db.execute(select(Game))
    return result.scalars().all()

async def get_game_by_id(db: AsyncSession, game_id: int):
    result = await db.execute(select(Game).where(Game.id == game_id))
    return result.scalar_one_or_none()

async def search_games(db: AsyncSession, term: str):
    result = await db.execute(select(Game).where(Game.title.ilike(f"%{term}%")))
    return result.scalars().all()