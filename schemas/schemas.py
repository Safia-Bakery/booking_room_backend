import re
from datetime import datetime
from typing import List, Optional, Union

from fastapi.params import Form
from pydantic import BaseModel, ConfigDict, EmailStr
from config.config import SECRET_KEY


# pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GetUserRole(TunedModel):
    id: int
    role: str
    permissions: List[str]


class CreateUserRole(BaseModel):
    role: str
    permissions: List[str]


class GetRoom(TunedModel):
    id: int
    name: str


class CreateRoom(BaseModel):
    name: str


class GetUser(TunedModel):
    id: str
    role_id: Optional[int] = None
    fullname: str
    email: str
    reg_date: datetime = datetime.now()
    update_date: datetime = datetime.now()
    google_token: Optional[str]


class CreateUser(BaseModel):
    id: str
    role_id: Optional[int] = None
    fullname: Optional[str]
    email: EmailStr


class GoogleToken(BaseModel):
    token: str


class GetMeeting(TunedModel):
    id: Optional[str]
    room_id: int
    created_by: Optional[str] = None
    organizer: Optional[str] = None
    name: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]


class CreateMeeting(BaseModel):
    # id: Optional[int]
    room_id: int
    created_by: Optional[str] = None
    organizer: Optional[str] = None
    invited_users: Optional[List[EmailStr]] = None
    name: Optional[str] = None
    description: Optional[str]
    start_time: datetime
    end_time: datetime


class GetInvitation(TunedModel):
    id: int
    user: GetUser
    meeting: GetMeeting


class CreateInvitation(BaseModel):
    user_id: str
    meeting_id: int


class Token(TunedModel):
    email: str
    token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

