from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models import models
from sqlalchemy.exc import IntegrityError
from schemas.schemas import GetUserRole, CreateUpdateUserRole


def get_all_roles(db: Session):
    query = db.query(models.UserRole).all()
    return query


def create_role(db: Session, form_data: CreateUpdateUserRole):
    query = models.UserRole(role=form_data.role,
                            permissions=form_data.permissions)
    try:
        db.add(query)
        db.commit()
    except IntegrityError as e:
        db.rollback()

    return query
