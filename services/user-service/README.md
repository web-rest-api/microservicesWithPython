# user-service — reference implementation

Read this before building `game-service`. Every file below is annotated to explain its role. The structure you see here is the one you must replicate.

---

## Folder structure

```
user-service/
├── app/
│   ├── __init__.py        # empty, makes app a package
│   ├── main.py            # FastAPI app init, mounts the router
│   ├── database.py        # engine + session factory
│   ├── models.py          # SQLAlchemy ORM model (User)
│   ├── schemas.py         # Pydantic DTOs (UserCreate, UserOut)
│   ├── repository.py      # raw DB queries — no business logic here
│   ├── service.py         # business logic — calls repository
│   └── routes.py          # FastAPI router + endpoint handlers
├── alembic/
│   └── versions/          # auto-generated migration files go here
├── tests/
│   └── test_users.py
├── alembic.ini
├── requirements.txt
└── .env.example
```

---

## File-by-file breakdown

### `app/models.py` — ORM model

Defines the `users` table. This is the only file that knows about columns.

```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
```

---

### `app/schemas.py` — Pydantic DTOs

Two schemas: one for input, one for output. Keep them separate — the response shape is not always the same as the request shape.

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}
```

---

### `app/database.py` — engine + session

`get_db` is a FastAPI dependency. It opens a session before the request and closes it after.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")

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
from app.models import User
from app.schemas import UserCreate

def create_user(db: Session, data: UserCreate) -> User:
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def list_users(db: Session) -> list[User]:
    return db.query(User).all()
```

---

### `app/service.py` — business logic

Calls the repository and returns Pydantic schemas (not raw ORM objects) to the routes.

```python
from sqlalchemy.orm import Session
from app import repository
from app.schemas import UserCreate, UserOut

def add_user(db: Session, data: UserCreate) -> UserOut:
    user = repository.create_user(db, data)
    return UserOut.model_validate(user)

def fetch_user(db: Session, user_id: int) -> UserOut:
    user = repository.get_user(db, user_id)
    if user is None:
        raise ValueError(f"User {user_id} not found")
    return UserOut.model_validate(user)

def fetch_all_users(db: Session) -> list[UserOut]:
    users = repository.list_users(db)
    return [UserOut.model_validate(u) for u in users]
```

The `ValueError` raised here gets caught in `routes.py` and turned into an HTTP 404.

---

### `app/routes.py` — HTTP layer

One function per endpoint. Routes only call service functions — never the repository directly.

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import service, schemas

router = APIRouter(prefix="/v1/users", tags=["users"])

@router.post("/", response_model=schemas.UserOut, status_code=201)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.add_user(db, data)

@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return service.fetch_all_users(db)

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return service.fetch_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

---

### `app/main.py` — entry point

```python
from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="user-service")
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
DATABASE_URL=sqlite:///./users.db
```

Copy to `.env` before running. Never commit `.env`.
