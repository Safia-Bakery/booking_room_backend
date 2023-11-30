from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status

from models import models
from sqlalchemy.exc import IntegrityError
from schemas.schemas import GetUserRole, CreateUpdateUserRole, SignUpUser, LoginUser


def get_all_roles(db: Session):
    query = db.query(models.UserRole).all()
    return query


def create_role(db: Session, form_data: CreateUpdateUserRole):
    query = models.UserRole(role=form_data.role,
                            permissions=form_data.permissions)
    try:
        db.add(query)
        db.commit()
    except IntegrityError:
        db.rollback()
        return HTTPException(status_code=status.HTTP_302_FOUND, detail="User role with the name already exists!")

    return query


def get_user(db: Session, form_data: LoginUser):
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
    except IntegrityError as ex:
        db.rollback()
        return HTTPException(status_code=status.HTTP_302_FOUND, detail='User with the email already exists!')

    return query
