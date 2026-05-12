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
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime, timezone
import uuid
from app.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    release_year = Column(Integer, nullable=True)
    cover_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
```

---

### `app/schemas.py` — Pydantic DTOs

`GameCreate` = what comes **in**. `GameOut` = what goes **out**. Keep them separate.

```python
from pydantic import BaseModel
from datetime import datetime

class GameCreate(BaseModel):
    title: str
    genre: str
    platform: str
    release_year: int | None = None
    cover_url: str | None = None

class GameOut(BaseModel):
    id: str
    title: str
    genre: str
    platform: str
    release_year: int | None
    cover_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

class GameList(BaseModel):
    """Paginated envelope — all list endpoints return this shape."""
    items: list[GameOut]
    total: int
    limit: int
    offset: int
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

def get_game(db: Session, game_id: str) -> Game | None:
    ...

def list_games(db: Session, limit: int = 20, offset: int = 0) -> tuple[list[Game], int]:
    ...

def search_games(db: Session, q: str, limit: int = 20, offset: int = 0) -> tuple[list[Game], int]:
    # hint: use .filter(Game.title.ilike(f"%{q}%"))
    ...
```

---

### `app/service.py` — business logic

Calls the repository and returns Pydantic schemas (not raw ORM objects) to the routes.

```python
from sqlalchemy.orm import Session
from app import repository
from app.schemas import GameCreate, GameOut, GameList

def add_game(db: Session, data: GameCreate) -> GameOut:
    ...

def fetch_game(db: Session, game_id: str) -> GameOut:
    # raise ValueError if not found — routes.py turns it into a 404
    ...

def fetch_all_games(db: Session, limit: int = 20, offset: int = 0) -> GameList:
    ...

def find_games(db: Session, q: str, limit: int = 20, offset: int = 0) -> GameList:
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

@router.get("/", response_model=schemas.GameList)
def list_games(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    ...

@router.get("/search", response_model=schemas.GameList)
def search_games(q: str, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    ...

@router.get("/{game_id}", response_model=schemas.GameOut)
def get_game(game_id: str, db: Session = Depends(get_db)):
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
