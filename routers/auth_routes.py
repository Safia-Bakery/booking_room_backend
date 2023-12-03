import re
from typing import List
from fastapi import APIRouter, status, Depends
from config.db import SessionLocal
from sqlalchemy.orm import Session
from models.models import UserRole, User
from schemas.schemas import SignUpUser, GetUser
from crud import crud
from fastapi.exceptions import HTTPException

from utils.utils import get_db


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


# fake_users = [
#     {"id": 1, "fullname": "Bakhtiyor Bakhriddinov", "phone": "+998977828474", "email": "uzdev27@gmail.com"},
#     {"id": 2, "fullname": "Bekzod Sagdullayev", "phone": "+998975564455", "email": "uzbox21@gmail.com"},
#     {"id": 3, "fullname": "Ilkhom Aliev", "phone": "+998971156455", "email": "uzlive11@gmail.com"}
# ]


@auth_router.post("/signup", response_model=GetUser, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpUser, db: Session = Depends(get_db)):
    created_user = crud.create_user(db=db, form_data=user)
    if not created_user:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='User with the email already exists!')
    return created_user


# @auth_router.post("/login", response_model=LoginUser, status_code=200)
# async def login(user: LoginUser, db: Session = Depends(get_db)):
#     user_obj = crud.login_user(db=session, form_data=user)
#     if user_obj:
#         access_token = authorize.create_access_token(subject=user_obj.email)
#         refresh_token = authorize.create_refresh_token(subject=user_obj.email)
#
#         response = {
#             "access": access_token,
#             "refresh": refresh_token
#         }
#         return jsonable_encoder(response)
#         print(user_obj)
#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Entered invalid email")


