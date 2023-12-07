from fastapi import HTTPException, status
from sqlalchemy import and_, cast, Date
from sqlalchemy.orm import Session
from models import models
from sqlalchemy.exc import IntegrityError
from schemas.schemas import *
from datetime import datetime


# ----------------------- USER ROLES OPERATIONS ------------------------------------
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
    else:
        return query


def delete_role(id, db: Session):
    query = db.query(models.UserRole).filter(models.UserRole.id == id).delete(synchronize_session=False)
    db.commit()
    return query


def update_role(db: Session, id, role: CreateUserRole):
    obj = db.query(models.UserRole).filter(models.UserRole.id == id).update(dict(role))
    db.commit()
    return obj


# ----------------------- ROOMS OPERATIONS ------------------------------------
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
    else:
        return query


# ----------------------- USERS OPERATIONS ------------------------------------
def get_all_users(db: Session):
    query = db.query(models.User).all()
    return query


def get_user(id, db: Session):
    query = db.query(models.User).get(id)
    # query = db.query(models.User).filter(models.User.id == id).first()
    return query


def check_email(db: Session, email):
    query = db.query(models.User).filter(models.User.email == email).first()
    return query


def create_user(db: Session, form_data):
    query = models.User(id=form_data['sub'],
                        fullname=form_data['name'],
                        email=form_data['email']
                        )
    try:
        db.add(query)
        db.commit()
        db.refresh(query)
    except IntegrityError:
        db.rollback()
    else:
        return query


def get_or_create_user(db: Session, form_data):
    query = db.query(models.User).filter(models.User.email == form_data['email']).first()
    if query:
        return query

    query = models.User(id=form_data['id'],
                        fullname=form_data['name'],
                        email=form_data['email']
                        )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


# ----------------------- MEETINGS OPERATIONS ------------------------------------
def get_all_meetings(db: Session):
    query = db.query(models.Meeting).all()
    return query


def get_all_meetings_of_room_by_date(room_id, date, db: Session):
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
    else:
        return query


# ----------------------- INVITATIONS OPERATIONS ------------------------------------
def get_all_user_invitations(user_id, db: Session):
    query = db.query(models.Invitation).filter(models.Invitation.user_id == user_id)
    return query


def create_invitations(db: Session, user_id, meeting_id, room_id):
    query = models.Invitation(user_id=user_id,
                              meeting_id=meeting_id,
                              room_id=room_id
                              )
    try:
        db.add(query)
        db.commit()
        db.refresh(query)
    except IntegrityError:
        db.rollback()
    else:
        return query
