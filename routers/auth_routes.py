import re
from typing import List
from fastapi import APIRouter, status, Depends
from config.db import SessionLocal
from models.models import UserRole, User
from schemas.schemas import SignUpUser, LoginUser
from crud import crud
from fastapi.exceptions import HTTPException
# from fastapi_jwt_auth import AuthJWT
# from fastapi.encoders import jsonable_encoder


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
session = SessionLocal()


# fake_users = [
#     {"id": 1, "fullname": "Bakhtiyor Bakhriddinov", "phone": "+998977828474", "email": "uzdev27@gmail.com"},
#     {"id": 2, "fullname": "Bekzod Sagdullayev", "phone": "+998975564455", "email": "uzbox21@gmail.com"},
#     {"id": 3, "fullname": "Ilkhom Aliev", "phone": "+998971156455", "email": "uzlive11@gmail.com"}
# ]


@auth_router.post("/signup", response_model=SignUpUser, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpUser):
    return crud.create_user(db=session, form_data=user)


# @auth_router.post("/login", response_model=LoginUser, status_code=200)
# async def login(user: LoginUser, authorize: AuthJWT = Depends()):
#     pass
    # user_obj = crud.get_user(db=session, form_data=user)
    # if user_obj:
    #     # access_token = authorize.create_access_token(subject=user_obj.email)
    #     # refresh_token = authorize.create_refresh_token(subject=user_obj.email)
    #     #
    #     # response = {
    #     #     "access": access_token,
    #     #     "refresh": refresh_token
    #     # }
    #     # return jsonable_encoder(response)
    #     print(user_obj)
    # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Entered invalid email")


# @auth_router.get("/users")
# def get_users(limit: int, offset: int):
#     return fake_users[offset:][:limit]


# @auth_router.get("/users/{user_id}", response_model=List[GetUser])
# def get_user(user_id: int):
#     return [user for user in fake_users if user["id"] == user_id]
#     # return user_id



# @auth_router.post("/users/{user_id}")
# def change_username(user_id: int, new_name: str):
#     current_user = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
#     current_user["fullname"] = new_name
#     return {"status": 200, "data": current_user}
