import re
from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from schemas.schemas import *
from crud import crud
from utils.utils import get_db, get_current_user, email_sender
from datetime import datetime, date

app_router = APIRouter(
    prefix='/app',
    tags=['app']
)


# ----------------------- Actions with ROOMS ------------------------
@app_router.get("/rooms", response_model=List[GetRoom], status_code=200)
async def get_rooms(db: Session = Depends(get_db), current_user: GetUser = Depends(get_current_user)):
    return crud.get_all_rooms(db=db)


@app_router.get("/rooms/{id}", response_model=GetRoom, status_code=200)
async def get_room(id: int, response: Response, db: Session = Depends(get_db),
                   current_user: GetUser = Depends(get_current_user)):
    room = crud.get_room(id=id, db=db)
    if not room:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room with the id not found!")
    return room


# --------------------- Actions with MEETINGS --------------------------
@app_router.get("/meetings", response_model=List[GetMeeting], status_code=200)
def get_meetings_of_room(room_id: int, query_date: date, db: Session = Depends(get_db),
                         current_user: GetUser = Depends(get_current_user)):
    specific_meetings = crud.get_all_meetings_of_room_by_date(room_id=room_id, date=query_date, db=db)
    if not specific_meetings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planed meetings not found!")
    return specific_meetings


@app_router.post("/meetings", response_model=CreateMeeting, status_code=201)
async def create_meeting(form_data: CreateMeeting, db: Session = Depends(get_db),
                         current_user: GetUser = Depends(get_current_user)):
    role_id = current_user.role_id
    if not role_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissions denied!")
    role_name = crud.get_role(role_id, db).role
    if role_name == "organizer":
        created_meeting = crud.create_meeting(db=db, form_data=form_data)
        if not created_meeting:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="The meeting with id already exists!")
        return created_meeting
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissions denied to create meeting!")


# ----------------- Actions with INVITATIONS -----------------------
@app_router.post("/invitations", response_model=CreateInvitation, status_code=201)
async def create_invitation(form_data: CreateInvitation, db: Session = Depends(get_db),
                            current_user: GetUser = Depends(get_current_user)):
    role_id = current_user.role_id
    if not role_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissions denied!")
    role_name = crud.get_role(role_id, db).role
    email_receivers = [current_user.email]
    if role_name == "organizer":
        for id in form_data.user_id:
            created_invitation = crud.create_invitations(db=db, user_id=id, meeting_id=form_data.meeting_id,
                                                         room_id=form_data.room_id)
            if not created_invitation:
                raise HTTPException(status_code=status.HTTP_302_FOUND, detail="The invitation with id already exists!")
            user_email = crud.get_user(id=id, db=db).email
            email_receivers.append(user_email)
        room = crud.get_room(id=form_data.room_id, db=db).name
        meeting_name = crud.get_meeting(id=form_data.meeting_id, db=db).name
        start_time = crud.get_meeting(id=form_data.meeting_id, db=db).start_time
        end_time = crud.get_meeting(id=form_data.meeting_id, db=db).end_time
        await email_sender(receivers=email_receivers, organizer=current_user.fullname, room=room,
                           meeting_name=meeting_name, start_time=start_time, end_time=end_time)

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissions denied to create invitation!")


@app_router.get("/invitations", response_model=List[GetInvitation])
async def get_invitations(user_id: int, db: Session = Depends(get_db),
                          current_user: GetUser = Depends(get_current_user)):
    return crud.get_all_user_invitations(user_id=user_id, db=db)
