from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy import cast, Date, Time
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
# from bson import json_util
import json
import uuid
from schemas.schemas import *
from crud import crud
from utils.bot_requests import send_to_chat
from utils.utils import get_db, get_current_user, email_sender
from utils.google_calendar import get_events, create_event, delete_event
from datetime import datetime, date
from config.config import BOT_TOKEN, CHANNEL_ID


app_router = APIRouter(
    prefix='/app',
    tags=['app']
)


# ----------------------- Actions with USERS ------------------------
@app_router.get("/users", response_model=List[GetUser], status_code=200)
async def get_users(db: Session = Depends(get_db), current_user: GetUser = Depends(get_current_user)):
    return crud.get_all_users(db=db)


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
def get_meetings_of_room(room_id: int, query_date: Optional[date], db: Session = Depends(get_db),
                         current_user: GetUser = Depends(get_current_user)):
    if not query_date:
        all_meetings = crud.get_all_meetings_of_room(room_id=room_id, db=db)
        return all_meetings
    specific_meetings = crud.get_all_meetings_of_room_by_date(room_id=room_id, date=query_date, db=db)
    if not specific_meetings:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Planed meetings not found!")
        return JSONResponse([])
    return specific_meetings


@app_router.get("/meetings/{id}", response_model=GetMeeting, status_code=200)
async def get_meeting(id: str, response: Response, db: Session = Depends(get_db)):  # current_user: GetUser = Depends(get_current_user)
    meeting = crud.get_meeting(id=id, db=db)
    if not meeting:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting with the id not found!")
    return meeting


@app_router.get("/my-meetings", response_model=List[GetMeeting])
async def get_own_meetings(db: Session = Depends(get_db), current_user: GetUser = Depends(get_current_user)):  # user_id: int,
    return crud.get_all_user_meetings(user_id=current_user.id, db=db)


@app_router.post("/meetings", response_model=CreateMeeting, status_code=201)
async def create_meeting(form_data: CreateMeeting, db: Session = Depends(get_db), current_user: GetUser = Depends(get_current_user)):
    existed_meeting = crud.check_meeting(db=db, form_data=form_data)
    if existed_meeting:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Конференц зал уже забронирован в указанном периоде времени!")
    meeting_id = uuid.uuid4().hex
    created_meeting = crud.create_meeting(db=db, form_data=form_data, meeting_id=meeting_id, creator=current_user.id)
    google_token = current_user.google_token
    email_receivers = []
    if not form_data.invited_users:
        return created_meeting

    # there will be created google calendar event
    for user_email in form_data.invited_users:
        created_invitation = crud.create_invitations(db=db, user_email=user_email, meeting_id=created_meeting.id)
        if not created_invitation:
            continue
        email_receivers.append({"email": user_email})
    room = crud.get_room(id=form_data.room_id, db=db).name
    organizer = created_meeting.organizer
    title = created_meeting.description
    start_time = created_meeting.start_time
    end_time = created_meeting.end_time
    # message_text = (f"You were invited to meeting {title} organized by {organizer}.\n"
    #                 f"Meeting get place in {room} at {start_time.split(sep='.')[0]} and "
    #                 f"continue until {end_time.split(sep='.')[0]}")
    meeting_date = str(start_time.date())
    meeting_start_time = str(start_time.time().strftime("%H:%M"))
    meeting_end_time = str(end_time.time().strftime("%H:%M"))
    message_text = (f"Уважаемые коллеги!\n\n{meeting_date} с {meeting_start_time} до {meeting_end_time}"
                    f" {room} будет забронирована✅.\n\n"
                    f"Забронировал: {organizer}")
    # await email_sender(receivers=email_receivers, organizer=created_meeting.organizer, room=room,
    #                    meeting_name=meeting_name, start_time=start_time, end_time=end_time)
    await create_event(google_token=google_token, id=meeting_id, organizer=organizer, room=room, title=title,
                       start_time=start_time, end_time=end_time, guests=email_receivers, message_text=message_text)
    print(BOT_TOKEN)
    print(CHANNEL_ID)
    print(message_text)
    await send_to_chat(bot_token=BOT_TOKEN, chat_id=CHANNEL_ID, message_text=message_text)

    return created_meeting


@app_router.delete("/meetings/{id}", status_code=204)
async def delete_meeting(id, db: Session = Depends(get_db), current_user: GetUser = Depends(get_current_user)):
    deleted_meeting = crud.delete_own_meeting(id=id, user_id=current_user.id, db=db)
    if not deleted_meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found or not have permission!")
    await delete_event(id=deleted_meeting.id, google_token=current_user.google_token)
    return deleted_meeting


@app_router.put("/meetings/{id}", status_code=202)
async def update_meeting(id, meeting: CreateMeeting, db: Session = Depends(get_db), current_user: GetUser = Depends(get_current_user)):
    updated_meeting = crud.update_meeting(id=id, meeting=meeting, db=db)
    if not updated_meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found!!")

    return updated_meeting


# ----------------- Actions with INVITATIONS -----------------------
# @app_router.post("/invitations", response_model=CreateInvitation, status_code=201)
# async def create_invitation(form_data: CreateInvitation, db: Session = Depends(get_db),
#                             current_user: GetUser = Depends(get_current_user)):
#     email_receivers = [current_user.email]
#     for id in form_data.user_id:
#         created_invitation = crud.create_invitations(db=db, user_id=id, meeting_id=form_data.meeting_id)
#         if not created_invitation:
#             raise HTTPException(status_code=status.HTTP_302_FOUND, detail="The invitation with id already exists!")
#         user_email = crud.get_user(id=id, db=db).email
#         email_receivers.append(user_email)
#     room = crud.get_room(id=form_data.room_id, db=db).name
#     meeting_name = crud.get_meeting(id=form_data.meeting_id, db=db).name
#     start_time = crud.get_meeting(id=form_data.meeting_id, db=db).start_time
#     end_time = crud.get_meeting(id=form_data.meeting_id, db=db).end_time
#     await email_sender(receivers=email_receivers, organizer=current_user.fullname, room=room,
#                        meeting_name=meeting_name, start_time=start_time, end_time=end_time)


@app_router.get("/invitations", response_model=List[GetInvitation])
async def get_invitations(db: Session = Depends(get_db), current_user: GetUser = Depends(get_current_user)):  # user_id: int
    return crud.get_all_user_invitations(user_id=current_user.id, db=db)
