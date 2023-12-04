import re
from typing import List
from fastapi import APIRouter, status, Depends
from config.db import SessionLocal
from sqlalchemy.orm import Session
from models.models import UserRole, User
from schemas.schemas import *
from crud import crud
from fastapi.exceptions import HTTPException

from utils.utils import get_db, get_current_user


admin_router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


# --------------------- Actions with ROLES --------------------------
@admin_router.get("/roles", response_model=List[GetUserRole], status_code=200)
async def get_roles(db: Session = Depends(get_db), current_user: GetUser = Depends(get_current_user)):
    return crud.get_all_roles(db=db)


@admin_router.get("/roles/{id}", response_model=GetUserRole, status_code=200)
async def get_role(id, db: Session = Depends(get_db)):
    role = crud.get_role(id=id, db=db)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found!")
    return role


@admin_router.post("/roles", response_model=GetUserRole, status_code=201)
async def create_role(form_data: CreateUserRole, db: Session = Depends(get_db)):
    created_role = crud.create_role(db=db, form_data=form_data)
    if not created_role:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="User role with the name already exists!")
    return created_role


@admin_router.delete("/roles/{id}", status_code=204)
async def delete_role(id, db: Session = Depends(get_db)):
    deleted_role = crud.delete_role(id=id, db=db)
    if not deleted_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User role not found!")
    return deleted_role


@admin_router.put("/roles/{id}", status_code=202)
async def update_role(id, role: CreateUserRole, db: Session = Depends(get_db)):
    updated_role = crud.update_role(db=db, id=id, role=role)
    if not updated_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User role with the id not found!")

    return updated_role


# ----------------------- Actions with ROOMS ------------------------
@admin_router.get("/rooms", response_model=List[GetRoom], status_code=200)
async def get_rooms(db: Session = Depends(get_db)):
    return crud.get_all_rooms(db=db)


@admin_router.get("/rooms/{id}", response_model=GetRoom, status_code=200)
async def get_room(id, db: Session = Depends(get_db)):
    room = crud.get_room(id=id, db=db)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with the id {id} not found!")
    return room


@admin_router.post("/rooms", response_model=CreateRoom, status_code=201)
async def create_room(form_data: CreateRoom, db: Session = Depends(get_db)):
    created_room = crud.create_room(db=db, form_data=form_data)
    if not created_room:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="The room with the name already exists!")
    return created_room


# --------------------- Actions with USERS --------------------------
@admin_router.get("/users", response_model=List[GetUser], status_code=200)
async def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db=db)


@admin_router.get("/users/{id}", response_model=GetUser, status_code=200)
def get_user(id, db: Session = Depends(get_db)):
    user = crud.get_user(id=id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found!")
    return user


# --------------------- Actions with MEETINGS --------------------------
@admin_router.get("/meetings", response_model=List[GetMeeting], status_code=200)
async def get_meetings(db: Session = Depends(get_db)):
    return crud.get_all_meetings(db=db)


@admin_router.get("/meetings/{id}", response_model=GetMeeting, status_code=200)
def get_meeting(id, db: Session = Depends(get_db)):
    meeting = crud.get_meeting(id=id, db=db)
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Meeting with the id {id} not found!")
    return meeting

