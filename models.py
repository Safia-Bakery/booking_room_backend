from datetime import datetime

from sqlalchemy import MetaData, types, ForeignKey, Table, Column

from pydantic import BaseModel, Field


metadata = MetaData()


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


# class User(BaseModel):
#     id: int
#     fullname: str
#     phone: str = Field(min_length=9, max_length=13)
#     email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
