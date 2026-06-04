from sqlalchemy.orm import Session
from app.repository import get_users

def fetch_users(db: Session):
    return get_users(db)
