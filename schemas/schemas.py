import re
from datetime import datetime
from typing import List, Optional, Union

from fastapi import UploadFile, File
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


class CreateUserRole(TunedModel):
    role: str
    permissions: List[str]


class GetRoom(TunedModel):
    id: int
    name: str
    location: Optional[int] = None
    image: Optional[str] = None


class CreateRoom(TunedModel):
    name: str
    location: int
    image: str


class UpdateRoom(TunedModel):
    id: int
    name: Optional[str] = None
    location: Optional[int] = None
    image: Optional[str] = None


class GetUser(TunedModel):
    id: Optional[str]
    role_id: Optional[int] = None
    fullname: Optional[str]
    email: Optional[str]
    reg_date: Optional[datetime] = datetime.now()
    update_date: Optional[datetime] = datetime.now()
    google_token: Optional[str]


class CreateUser(BaseModel):
    id: str
    role_id: Optional[int] = None
    fullname: Optional[str]
    email: EmailStr


class GoogleToken(BaseModel):
    token: str


class GetInvitationList(TunedModel):
    user: Optional[List[GetUser]] = None


class GetInvitation(TunedModel):
    user_email: Optional[EmailStr] = None


class GetMeeting(TunedModel):
    id: Optional[str]
    room_id: int
    created_by: Optional[str] = None
    organizer: Optional[str] = None
    name: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    # invitation: Optional[List[GetInvitationList]] = None
    invitation: Optional[List[GetInvitation]] = None


class CreateMeeting(BaseModel):
    # id: Optional[str]
    room_id: int
    created_by: Optional[str] = None
    organizer: Optional[str] = None
    invited_users: Optional[List[EmailStr]] = None
    name: Optional[str] = None
    description: Optional[str]
    start_time: datetime
    end_time: datetime


class CreateInvitation(BaseModel):
    user_id: str
    meeting_id: int


class Token(TunedModel):
    email: str
    token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

