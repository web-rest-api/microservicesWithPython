from sqlalchemy.orm import Session

from app import repository
from app.schemas import UserCreate, UserOut, UserList


def add_user(db: Session, data: UserCreate) -> UserOut:
    user = repository.create_user(db, data)
    return UserOut.model_validate(user)


def fetch_user(db: Session, user_id: str) -> UserOut:
    user = repository.get_user(db, user_id)

    if user is None:
        raise ValueError(f"User {user_id} not found")

    return UserOut.model_validate(user)


def fetch_all_users(
    db: Session,
    limit: int = 20,
    offset: int = 0,
) -> UserList:
    users, total = repository.list_users(
        db,
        limit=limit,
        offset=offset,
    )

    return UserList(
        items=[UserOut.model_validate(u) for u in users],
        total=total,
        limit=limit,
        offset=offset,
    )