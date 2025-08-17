from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.api.dependencies import get_current_user
from app.models import User
from app.db.session import get_db


router = APIRouter()


@router.get('/me', response_model=UserResponse)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put('/me', status_code=status.HTTP_200_OK)
async def update_me(update_data: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if update_data.username is not None:
        current_user.username = update_data.username
    if update_data.first_name is not None:
        current_user.first_name = update_data.first_name
    if update_data.last_name is not None:
        current_user.last_name = update_data.last_name

    # commit changes to the database
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return current_user



@router.post('/reset-password', status_code=status.HTTP_200_OK)
async def reset_password(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    pass



@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    db.delete(current_user)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content={"message": "User deleted successfully"})







