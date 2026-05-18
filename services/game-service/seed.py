import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine
from app.models import Base, Game

GAMES = [
    {"title": "Cyber Odyssey",    "genre": "RPG",     "description": "An open-world cyberpunk adventure."},
    {"title": "Shadow Tactics",   "genre": "Strategy","description": "Stealth-based tactical warfare."},
    {"title": "Pixel Dungeon X",  "genre": "Roguelike","description": "Procedurally generated dungeons."},
    {"title": "Turbo Racers",     "genre": "Racing",  "description": "High-speed futuristic racing."},
    {"title": "Galaxy Defenders", "genre": "Shooter", "description": "Co-op space shooter."},
]

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    imported = 0
    for data in GAMES:
        existing = db.query(Game).filter(Game.title == data["title"]).first()
        if existing:
            continue
        game = Game(
            title=data["title"],
            genre=data["genre"],
            description=data["description"],
        )
        db.add(game)
        imported += 1
    db.commit()
    db.close()
    print(f"Imported {imported} games.")

if __name__ == "__main__":
    run()