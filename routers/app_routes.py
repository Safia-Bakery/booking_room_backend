import re
from typing import List
from fastapi import APIRouter
from config.db import SessionLocal
from models.models import UserRole
from schemas.schemas import GetUser, RoomSchema, GetUserRole, MeetingSchema, InvitationSchema, CreateUpdateUserRole
from crud import crud

app_router = APIRouter()
session = SessionLocal()


@app_router.get("/roles", response_model=List[GetUserRole])
async def get_roles():
    return crud.get_all_roles(db=session)


@app_router.post("/role", response_model=GetUserRole)
async def create_role(form_data: CreateUpdateUserRole):
    return crud.create_role(db=session, form_data=form_data)


@app_router.get("/rooms")
async def get_users(rooms: List[RoomSchema]):
    return {"status": 200, "data": rooms}
    # must be crud function responses
