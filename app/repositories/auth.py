from sqlalchemy import select
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, user: User) -> User:
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(error))



def get_user_by_id(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalars().first()

def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalars().first()

def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalars().first()

