from fastapi import HTTPException, status
from sqlalchemy import and_, cast, Date
from sqlalchemy.orm import Session
from models import models
from sqlalchemy.exc import IntegrityError
from schemas.schemas import *
from datetime import datetime


def get_all_roles(db: Session):
    query = db.query(models.UserRole).all()
    return query


def get_role(id, db: Session):
    query = db.query(models.UserRole).get(id)
    return query


def create_role(db: Session, form_data: CreateUserRole):
    query = models.UserRole(role=form_data.role,
                            permissions=form_data.permissions)
    try:
        db.add(query)
        db.commit()
        db.refresh(query)
    except IntegrityError:
        db.rollback()
        return HTTPException(status_code=status.HTTP_302_FOUND, detail="User role with the name already exists!")

    return query


def get_all_rooms(db: Session):
    query = db.query(models.Room).all()
    return query


def get_room(id, db: Session):
    query = db.query(models.Room).get(id)
    return query


def create_room(db: Session, form_data: CreateRoom):
    query = models.Room(name=form_data.name)
    try:
        db.add(query)
        db.commit()
        db.refresh(query)
    except IntegrityError:
        db.rollback()
        return HTTPException(status_code=status.HTTP_302_FOUND, detail="The room with the name already exists!")

    return query


def get_all_users(db: Session):
    query = db.query(models.User).all()
    return query


def get_user(id, db: Session):
    query = db.query(models.User).get(id)
    return query


def login_user(db: Session, form_data: LoginUser):
    query = db.query(models.User).filter(models.User.email == form_data.email).first()
    return query


def create_user(db: Session, form_data: SignUpUser):
    query = models.User(role_id=form_data.role_id,
                        fullname=form_data.fullname,
                        email=form_data.email
                        )
    try:
        db.add(query)
        db.commit()
        db.refresh(query)
    except IntegrityError as ex:
        db.rollback()
        return HTTPException(status_code=status.HTTP_302_FOUND, detail='User with the email already exists!')

    return query


def get_all_meetings(db: Session):
    query = db.query(models.Meeting).all()
    return query


def get_all_meetings_of_room_by_date(room_id, date, db: Session):
    datetime()
    query = db.query(models.Meeting).filter(models.Meeting.room_id == room_id).filter(models.Meeting.start_time.cast(Date) == date)
    return query


def get_meeting(id, db: Session):
    query = db.query(models.Meeting).get(id)
    return query


def create_meeting(db: Session, form_data: CreateMeeting):
    query = models.Meeting(room_id=form_data.room_id,
                           organized_by=form_data.organized_by,
                           name=form_data.name,
                           description=form_data.description,
                           start_time=form_data.start_time,
                           end_time=form_data.end_time
                           )
    try:
        db.add(query)
        db.commit()
        db.refresh(query)
    except IntegrityError:
        db.rollback()
        return HTTPException(status_code=status.HTTP_302_FOUND, detail="The Meeting already exists!")

    return query


def get_all_user_invitations(user_id, db: Session):
    query = db.query(models.Meeting).filter(models.Invitation.user_id == user_id)
    return query


def create_invitations(db: Session, form_data: CreateInvitation):
    for id in form_data.user_id:
        query = models.Invitation(user_id=id,
                                  meeting_id=form_data.meeting_id,
                                  room_id=form_data.room_id
                                  )
        try:
            db.add(query)
            db.commit()
            db.refresh(query)
        except IntegrityError:
            db.rollback()
            return HTTPException(status_code=status.HTTP_302_FOUND, detail="The invitation already exists!")

    return True
