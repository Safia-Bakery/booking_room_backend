from datetime import datetime

from pydantic import BaseModel, Field


class UserRole(BaseModel):
    id: int
    role: str
    permissions: list[str]


class User(BaseModel):
    id: int
    role_id: int
    fullname: str
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    reg_date: datetime.timestamp = datetime.now()
    update_date: datetime.timestamp = datetime.now()


class Room(BaseModel):
    id: int
    name: str


class Meeting(BaseModel):
    id: int
    room_id: int
    organized_by: int
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    created_at: datetime


class Invitation(BaseModel):
    id: int
    user_id: User.id
    meeting_id: Meeting.id
    room_id: Room.id
