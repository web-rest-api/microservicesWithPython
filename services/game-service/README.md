# game-service — your implementation

This is the service you build in Module 2. Use `services/user-service/README.md` as your working reference — the structure is identical, only the entity changes.

---

## Folder structure

```
game-service/
├── app/
│   ├── __init__.py        # empty, makes app a package
│   ├── main.py            # FastAPI app init, mounts the router
│   ├── database.py        # engine + session factory
│   ├── models.py          # SQLAlchemy ORM model (Game)
│   ├── schemas.py         # Pydantic DTOs (GameCreate, GameOut)
│   ├── repository.py      # raw DB queries — no business logic here
│   ├── service.py         # business logic — calls repository
│   └── routes.py          # FastAPI router + endpoint handlers
├── alembic/
│   └── versions/          # auto-generated migration files go here
├── tests/
│   └── test_games.py
├── alembic.ini
├── requirements.txt
└── .env.example
```

---

## File-by-file breakdown

### `app/models.py` — ORM model

Defines the `games` table. This is the only file that knows about columns.

```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    cover_url = Column(String, nullable=True)
```

---

### `app/schemas.py` — Pydantic DTOs

`GameCreate` = what comes **in**. `GameOut` = what goes **out**. Keep them separate.

```python
from pydantic import BaseModel

class GameCreate(BaseModel):
    title: str
    genre: str
    platform: str
    cover_url: str | None = None

class GameOut(BaseModel):
    id: int
    title: str
    genre: str
    platform: str
    cover_url: str | None

    model_config = {"from_attributes": True}
```

---

### `app/database.py` — engine + session

`get_db` is a FastAPI dependency. It opens a session before the request and closes it after.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./games.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### `app/repository.py` — DB queries only

Functions here take a `Session` and return ORM objects. No HTTP, no business rules.

```python
from sqlalchemy.orm import Session
from app.models import Game
from app.schemas import GameCreate

def create_game(db: Session, data: GameCreate) -> Game:
    ...

def get_game(db: Session, game_id: int) -> Game | None:
    ...

def list_games(db: Session) -> list[Game]:
    ...

def search_games(db: Session, q: str) -> list[Game]:
    # hint: use .filter(Game.title.ilike(f"%{q}%"))
    ...
```

---

### `app/service.py` — business logic

Calls the repository and returns Pydantic schemas (not raw ORM objects) to the routes.

```python
from sqlalchemy.orm import Session
from app import repository
from app.schemas import GameCreate, GameOut

def add_game(db: Session, data: GameCreate) -> GameOut:
    ...

def fetch_game(db: Session, game_id: int) -> GameOut:
    # raise ValueError if not found — routes.py turns it into a 404
    ...

def fetch_all_games(db: Session) -> list[GameOut]:
    ...

def find_games(db: Session, q: str) -> list[GameOut]:
    ...
```

---

### `app/routes.py` — HTTP layer

One function per endpoint. Routes only call service functions — never the repository directly.

> **Order matters**: `/search` must be declared **before** `/{game_id}`, otherwise FastAPI will try to match the word "search" as an integer ID and return a 422.

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import service, schemas

router = APIRouter(prefix="/v1/games", tags=["games"])

@router.post("/", response_model=schemas.GameOut, status_code=201)
def create_game(data: schemas.GameCreate, db: Session = Depends(get_db)):
    ...

@router.get("/", response_model=list[schemas.GameOut])
def list_games(db: Session = Depends(get_db)):
    ...

@router.get("/search", response_model=list[schemas.GameOut])
def search_games(q: str, db: Session = Depends(get_db)):
    ...

@router.get("/{game_id}", response_model=schemas.GameOut)
def get_game(game_id: int, db: Session = Depends(get_db)):
    ...
```

---

### `app/main.py` — entry point

```python
from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="game-service")
app.include_router(router)
```

---

### `requirements.txt`

```
fastapi
uvicorn[standard]
sqlalchemy
alembic
pydantic
python-dotenv
aiosqlite
```

---

### `.env.example`

```
DATABASE_URL=sqlite:///./games.db
```

Copy to `.env` before running. Never commit `.env`.
