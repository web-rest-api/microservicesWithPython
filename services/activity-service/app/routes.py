from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import service
from app.schemas import ActivityCreate, ActivityOut, ActivityList

router = APIRouter(prefix="/v1/activities", tags=["activities"])

@router.post("/", status_code=201, response_model=ActivityOut)
async def create_activity(data: ActivityCreate, db: Session = Depends(get_db)):
    try:
        return await service.add_activity(db, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=ActivityList)
async def list_activities(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    return await service.fetch_all_activities(db, limit, offset)

@router.get("/user/{user_id}", response_model=ActivityList)
async def list_user_activities(user_id: str, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    return await service.fetch_user_activities(db, user_id, limit, offset)