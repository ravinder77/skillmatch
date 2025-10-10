from sqlalchemy import select
from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, user: User) -> User:
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User not found")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")



def get_by_id(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalars().first()

def get_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalars().first()

def get_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.scalar(stmt)

