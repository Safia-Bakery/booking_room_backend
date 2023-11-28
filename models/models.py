from datetime import datetime
from typing import Optional

from sqlalchemy import types, ForeignKey, Table, Column
from ormar import Model, fields, ModelMeta
from config.db import database, metadata

# class Base(DeclarativeBase):
#     pass



roles = Table(
    "roles",
    metadata,
    Column("id", types.Integer, primary_key=True, autoincrement=True),
    Column("role", types.String, nullable=False),
    Column("permissions", types.JSON, nullable=False)
)


users = Table(
    "users",
    metadata,
    Column("id", types.Integer, primary_key=True, autoincrement=True),
    Column("role_id", types.Integer, ForeignKey("roles.id"), nullable=False),
    Column("fullname", types.String, nullable=False),
    Column("phone", types.String, nullable=True),
    Column("email", types.String, nullable=False),
    Column("reg_date", types.TIMESTAMP, nullable=False, default=datetime.utcnow),
    Column("update_date", types.TIMESTAMP, nullable=False, default=datetime.utcnow)
)


# class User(SQLAlchemyBaseUserTable[int], Base):
#     id: int = Column(types.Integer, primary_key=True, autoincrement=True),
#     role_id: int = Column(types.Integer, ForeignKey("roles.id"), nullable=False),
#     fullname: str = Column(types.String, nullable=False),
#     email: str = Column(types.String(length=320), unique=True, index=True, nullable=False)
#     reg_date: datetime.timestamp = Column(types.DateTime(timezone=True), nullable=False)
#     update_date: datetime.timestamp = Column(types.String(length=320), unique=True, index=True, nullable=False)
#     hashed_password: str = Column(types.String(length=1024), nullable=False)
#     is_active: bool = Column(types.Boolean, default=True, nullable=False)
#     is_superuser: bool = Column(types.Boolean, default=False, nullable=False)
#     is_verified: bool = Column(types.Boolean, default=False, nullable=False)


class MainMeta(ModelMeta):
    class Meta:
        metadata = metadata
        database = database


class UserRole(Model):
    class Meta(MainMeta):
        pass

    id: int = fields.Integer(primary_key=True, nullable=False)
    role: str = fields.String(nullable=False)
    permissions: list[str] = fields.JSON(nullable=False)


class User(Model):
    id: int = fields.Integer(primary_key=True, nullable=False)
    role_id: Optional[UserRole] = fields.ForeignKey(UserRole)
    fullname: str = fields.String(nullable=False)
    email: str = fields.String(nullable=False)
    reg_date: datetime = fields.DateTime(default=datetime.now())
    update_date: datetime = fields.DateTime(default=datetime.now())


class Room(Model):
    class Meta(MainMeta):
        pass

    id: int = fields.Integer(primary_key=True, nullable=False)
    name: str = fields.String(nullable=False)


class Meeting(Model):
    class Meta(MainMeta):
        pass

    id: int = fields.Integer(primary_key=True, nullable=False)
    room_id: int = fields.Integer(nullable=False)
    organized_by: int = fields.Integer(nullable=False)
    name: str = fields.String()
    description: str = fields.Text()
    start_time: datetime = fields.DateTime(nullable=False)
    end_time: datetime = fields.DateTime(nullable=False)
    created_at: datetime = fields.DateTime(default=datetime.now())


class Invitation(Model):
    class Meta(MainMeta):
        pass

    id: int = fields.Integer(primary_key=True, nullable=False)
    user_id: int = fields.Integer(nullable=False)
    meeting_id: int = fields.Integer(nullable=False)
    room_id: int = fields.Integer(nullable=False)
