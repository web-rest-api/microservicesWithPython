from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
import app.service as service
import app.schemas as schemas

router = APIRouter(prefix="/v1/games", tags=["games"])

@router.post("", response_model=schemas.GameResponse)
async def create_game(game: schemas.GameCreate, db: AsyncSession = Depends(get_db)):
    return await service.add_game(db, game)

@router.get("", response_model=list[schemas.GameResponse])
async def list_games(db: AsyncSession = Depends(get_db)):
    return await service.list_games(db)

@router.get("/search", response_model=list[schemas.GameResponse])
async def search_games(q: str, db: AsyncSession = Depends(get_db)):
    return await service.search(db, q)

@router.get("/{id}", response_model=schemas.GameResponse)
async def get_game(id: int, db: AsyncSession = Depends(get_db)):
    game = await service.get_game(db, id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game