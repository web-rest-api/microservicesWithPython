from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.service import fetch_users

router = APIRouter(prefix="/v1/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def get_users(db: Session = Depends(get_db)):
    return fetch_users(db)
