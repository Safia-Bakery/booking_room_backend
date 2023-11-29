import re
from typing import List
from fastapi import APIRouter
from config.db import SessionLocal
from models.models import UserRole
from schemas.schemas import GetUser, RoomSchema, GetUserRole, MeetingSchema, InvitationSchema, CreateUpdateUserRole
from crud import crud


router = APIRouter()
session = SessionLocal()

fake_users = [
    {"id": 1, "fullname": "Bakhtiyor Bakhriddinov", "phone": "+998977828474", "email": "uzdev27@gmail.com"},
    {"id": 2, "fullname": "Bekzod Sagdullayev", "phone": "+998975564455", "email": "uzbox21@gmail.com"},
    {"id": 3, "fullname": "Ilkhom Aliev", "phone": "+998971156455", "email": "uzlive11@gmail.com"}
]


@router.get("/roles", response_model=GetUserRole)
def get_roles():
    return crud.get_all_roles(db=session)


@router.post("/role", response_model=GetUserRole)
def create_role(form_data: CreateUpdateUserRole):
    return crud.create_role(db=session, form_data=form_data)


@router.get("/users")
def get_users(limit: int, offset: int):
    return fake_users[offset:][:limit]


@router.get("/users/{user_id}", response_model=List[GetUser])
def get_user(user_id: int):
    return [user for user in fake_users if user["id"] == user_id]
    # return user_id


@router.post("/users")
def add_users(users: List[GetUser]):
    fake_users.extend(users)
    return {"status": 200, "data": fake_users}


@router.post("/users/{user_id}")
def change_username(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
    current_user["fullname"] = new_name
    return {"status": 200, "data": current_user}


@router.get("/rooms")
def get_users(rooms: List[RoomSchema]):
    return {"status": 200, "data": rooms}
    # must be crud function responses