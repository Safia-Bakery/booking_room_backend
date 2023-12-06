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
    id: int
    role_id: int
    role: GetUserRole
    fullname: str
    email: str
    reg_date: datetime = datetime.now()
    update_date: datetime = datetime.now()


class CreateUser(BaseModel):
    id: int
    role_id: Optional[int] = None
    fullname: Optional[str]
    email: EmailStr


class GoogleToken(BaseModel):
    token: str


class GetMeeting(TunedModel):
    id: int
    room_id: int
    organized_by: int
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    created_at: datetime = datetime.now()


class CreateMeeting(BaseModel):
    room_id: int
    organized_by: int
    name: Optional[str]
    description: Optional[str]
    start_time: datetime
    end_time: datetime


class GetInvitation(TunedModel):
    id: int
    user: GetUser
    meeting: GetMeeting
    room: GetRoom


class CreateInvitation(BaseModel):
    user_id: List[int]
    meeting_id: int
    room_id: int


class Token(TunedModel):
    id: int
    token: str


class TokenData(BaseModel):
    email: Optional[str] = None

