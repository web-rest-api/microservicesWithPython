# Infrastructure layer — ORM model.
#
# This is the only file that defines the shape of the `users` table.
# It maps Python attributes to database columns using SQLAlchemy.
#
# This file should:
# - Import Base from app.database
# - Define a User class with columns: id, username, email,
#   hashed_password, is_active, created_at
#
# Rule: no business logic here. This file only describes data structure.
#
# See the README for the full implementation.
from sqlalchemy import Column, Integer, String
from app.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    cover_url = Column(String, nullable=False)