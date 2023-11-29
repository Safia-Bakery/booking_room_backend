import re
from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, ConfigDict, EmailStr


# pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GetUserRole(TunedModel):
    role: str
    permissions: List[str]


class CreateUpdateUserRole(BaseModel):
    role: str
    permissions: List[str]


class GetUser(TunedModel):
    id: int
    role_id: int
    fullname: str
    email: str
    reg_date: datetime = datetime.now()
    update_date: datetime = datetime.now()


class CreateUpdateUser(BaseModel):
    id: int
    role_id: int
    fullname: str
    email: str
    reg_date: datetime = datetime.now()
    update_date: datetime = datetime.now()


class RoomSchema(TunedModel):
    id: int
    name: str


class MeetingSchema(TunedModel):
    id: int
    room_id: int
    organized_by: int
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    created_at: datetime = datetime.now()


class InvitationSchema(TunedModel):
    id: int
    user_id: GetUser
    meeting_id: MeetingSchema
    room_id: RoomSchema
