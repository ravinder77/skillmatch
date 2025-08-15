from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from starlette.responses import JSONResponse

from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.core.config import settings
from app.db.session import get_db
from app.models import User
from app.schemas.auth import AuthResponse, UserRole
from app.schemas.user import UserCreate
from app.models.user import User

router = APIRouter()

# OAUTH2 Password Flow

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserCreate, db: Session = Depends(get_db)):

    # check if username exists
   if db.query(User).filter(User.username == body.username).first():
       raise HTTPException(status_code=400, detail="Username already exists")

   # check if email is already registered
   if db.query(User).filter(User.email == body.email).first():
       raise HTTPException(status_code=400, detail="Email already registered")

    # hash password before saving to db
   hashed_pw = hash_password(body.password)

   new_user: User = User(
       username=body.username,
       first_name=body.first_name,
       last_name=body.last_name,
       email=str(body.email),
       hashed_password= hashed_pw,
       role= UserRole.USER,
       is_active=True
   )

   db.add(new_user)
   db.commit()
   db.refresh(new_user)

    # Generate JWT token
   token = create_access_token({
       'id':new_user.id,
       'email':new_user.email,
       'role':new_user.role.value
   })


   return AuthResponse(
       id=new_user.id,
       username=new_user.username,
       email=new_user.email,
       first_name=new_user.first_name,
       last_name=new_user.last_name,
       role=new_user.role.value,
       access_token=token,
   )






