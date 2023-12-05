import re
from datetime import timedelta
from typing import List
from fastapi import APIRouter, status, Depends, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from google.auth.transport import requests
from google.oauth2 import id_token
from starlette import status
from starlette.templating import Jinja2Templates
from config.config import ACCESS_TOKEN_EXPIRE_MINUTES, GOOGLE_CLIENT_ID
from config.db import SessionLocal
from sqlalchemy.orm import Session
from models.models import UserRole, User
from schemas.schemas import SignUpUser, GetUser, LoginUser, Token, TokenData
from crud import crud
from fastapi.exceptions import HTTPException

from utils.utils import get_db, create_access_token

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

templates = Jinja2Templates(directory="templates")
# fake_users = [
#     {"id": 1, "fullname": "Bakhtiyor Bakhriddinov", "phone": "+998977828474", "email": "uzdev27@gmail.com"},
#     {"id": 2, "fullname": "Bekzod Sagdullayev", "phone": "+998975564455", "email": "uzbox21@gmail.com"},
#     {"id": 3, "fullname": "Ilkhom Aliev", "phone": "+998971156455", "email": "uzlive11@gmail.com"}
# ]


# @auth_router.post("/signup", response_model=GetUser, status_code=status.HTTP_201_CREATED)
# async def signup(user: SignUpUser, db: Session = Depends(get_db)):
#     created_user = crud.create_user(db=db, form_data=user)
#     if not created_user:
#         raise HTTPException(status_code=status.HTTP_302_FOUND, detail='User with the email already exists!')
#     return created_user


async def google_auth(user: LoginUser):
    try:
        id_info = id_token.verify_oauth2_token(user.token, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bad code")

    user_id = None


@auth_router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(user: LoginUser, db: Session = Depends(get_db)):
    try:
        id_info = id_token.verify_oauth2_token(user.token, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bad code")
    created_user = crud.create_user(db=db, form_data=user)
    if not created_user:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='User with the email already exists!')
    # Generate JWT token and return
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": jsonable_encoder(access_token), "token_type": "bearer"}


@auth_router.get("/", response_model=Token, status_code=200)
async def google_auth_render(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})
