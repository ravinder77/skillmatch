from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.api.dependencies import get_current_user
from app.models import User
from app.db.session import get_db,


router = APIRouter()


@router.get('/me', response_model=UserResponse)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put('/me', response_model=UserUpdate)
async def update_me(update_data: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):



@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(current_user: User = Depends(get_current_user)):
    pass

