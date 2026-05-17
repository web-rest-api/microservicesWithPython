from sqlalchemy import Column, Integer, String
from app.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    platform = Column(String)
    cover_url = Column(String)