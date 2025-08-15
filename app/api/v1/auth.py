from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime

from starlette.responses import JSONResponse

from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.core.config import settings
from app.db.session import get_db
from app.schemas.auth import AuthResponse
from app.schemas.user import UserCreate
from app.models.user import User

router = APIRouter()

# OAUTH2 Password Flow

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserCreate, db: Session = Depends(get_db)):

   existing_username = db.query(User).filter(User.username == body.username).first()
   if existing_username:
       raise HTTPException(status_code=400, detail="Username already exists")
   # check if user with email exist
   user_with_email = db.query(User).filter(User.email == body.email).first()
   if user_with_email:
       raise HTTPException(status_code=400, detail="Email already registered")

   password = hash_password(body.password)

   new_user = User(
       username=body.username,
       first_name=body.first_name,
       last_name=body.last_name,
       email=str(body.email),
       hashed_password= password,
       role= "user" or body.role,
       is_active=True,
       created_at = datetime.now(),
       updated_at = datetime.now(),
   )

   db.add(new_user)
   db.commit()
   db.refresh(new_user)

   JSONResponse(new_user)






