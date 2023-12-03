import re
from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from schemas.schemas import *
from crud import crud
from utils.utils import get_db
from datetime import datetime, date

app_router = APIRouter(
    prefix='/app',
    tags=['app']
)


# ----------------------- Actions with ROOMS ------------------------
@app_router.get("/rooms", response_model=List[GetRoom], status_code=200)
async def get_rooms(db: Session = Depends(get_db)):
    return crud.get_all_rooms(db=db)


@app_router.get("/rooms/{id}", response_model=GetRoom, status_code=200)
async def get_room(id: int, response: Response, db: Session = Depends(get_db)):
    room = crud.get_room(id=id, db=db)
    if not room:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room with the id not found!")
    return room


# --------------------- Actions with MEETINGS --------------------------
@app_router.get("/meetings", response_model=List[GetMeeting], status_code=200)
def get_meetings_of_room(room_id: int, date: date, db: Session = Depends(get_db)):
    specific_meetings = crud.get_all_meetings_of_room_by_date(room_id=room_id, date=date, db=db)
    if not specific_meetings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planed meetings not found!")
    return specific_meetings


@app_router.post("/meetings", response_model=CreateMeeting, status_code=201)
async def create_meeting(form_data: CreateMeeting, db: Session = Depends(get_db)):
    created_meeting = crud.create_meeting(db=db, form_data=form_data)
    if not created_meeting:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="The meeting with id already exists!")
    return created_meeting


# ----------------- Actions with INVITATIONS -----------------------
@app_router.post("/invitations", response_model=CreateInvitation, status_code=201)
async def create_invitation(form_data: CreateInvitation, db: Session = Depends(get_db)):
    created_invitation = crud.create_invitations(db=db, form_data=form_data)
    return created_invitation


@app_router.get("/invitations", response_model=List[GetInvitation])
async def get_invitations(user_id: int, db: Session = Depends(get_db)):
    return crud.get_all_user_invitations(user_id=user_id, db=db)



