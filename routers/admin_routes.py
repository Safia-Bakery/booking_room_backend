import re
from typing import List
from fastapi import APIRouter, status, Depends
from config.db import SessionLocal
from sqlalchemy.orm import Session
from models.models import UserRole, User
from schemas.schemas import *
from crud import crud
from fastapi.exceptions import HTTPException

from utils.utils import get_db


admin_router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


# --------------------- Actions with ROLES --------------------------
@admin_router.get("/roles", response_model=List[GetUserRole])
async def get_roles(db: Session = Depends(get_db)):
    return crud.get_all_roles(db=db)


@admin_router.get("/roles/{id}", response_model=List[GetUserRole])
async def get_role(id, db: Session = Depends(get_db)):
    return crud.get_role(id=id, db=db)


@admin_router.post("/role", response_model=CreateUserRole)
async def create_role(form_data: CreateUserRole, db: Session = Depends(get_db)):
    return crud.create_role(db=db, form_data=form_data)


# ----------------------- Actions with ROOMS ------------------------
@admin_router.get("/rooms", response_model=List[GetRoom])
async def get_rooms(db: Session = Depends(get_db)):
    return crud.get_all_rooms(db=db)


@admin_router.get("/rooms/{id}", response_model=GetRoom)
async def get_room(id, db: Session = Depends(get_db)):
    return crud.get_room(id=id, db=db)


@admin_router.post("/room", response_model=CreateRoom)
async def create_room(form_data: CreateRoom, db: Session = Depends(get_db)):
    return crud.create_room(db=db, form_data=form_data)


# --------------------- Actions with USERS --------------------------
@admin_router.get("/users", response_model=List[GetUser])
async def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db=db)


@admin_router.get("/users/{id}", response_model=GetUser)
def get_user(id, db: Session = Depends(get_db)):
    return crud.get_user(id=id, db=db)


# --------------------- Actions with MEETINGS --------------------------
@admin_router.get("/meetings", response_model=List[GetMeeting])
async def get_meetings(db: Session = Depends(get_db)):
    return crud.get_all_meetings(db=db)


@admin_router.get("/meetings/{id}", response_model=GetMeeting)
def get_meeting(id, db: Session = Depends(get_db)):
    return crud.get_meeting(id=id, db=db)

