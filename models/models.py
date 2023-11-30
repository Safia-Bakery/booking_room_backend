from sqlalchemy import Integer, String, DateTime, JSON, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column

# from ormar import Model, ModelMeta, Integer, String, DateTime, Text, ForeignKey, JSON
# from config.db import metadata


# class MainMeta(ModelMeta):
#     class Meta:
#         metadata = metadata
#         database = database


Base = declarative_base()


class UserRole(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    role = Column(String, unique=True, nullable=False)
    permissions = Column(ARRAY(String), nullable=False)
    user = relationship('User', back_populates='role')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    reg_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now())
    role = relationship('UserRole', back_populates='user')
    meeting = relationship('Meeting', back_populates='user')
    invitation = relationship('Invitation', back_populates='user')


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    meeting = relationship('Meeting', back_populates='room')
    invitation = relationship('Invitation', back_populates='room')


class Meeting(Base):
    __tablename__ = 'meetings'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    organized_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    room = relationship('Room', back_populates='meeting')
    user = relationship('User', back_populates='meeting')
    invitation = relationship('Invitation', back_populates='meeting')


class Invitation(Base):
    __tablename__ = 'invitations'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user = relationship('User', back_populates='invitation')
    meeting = relationship('Meeting', back_populates='invitation')
    room = relationship('Room', back_populates='invitation')
