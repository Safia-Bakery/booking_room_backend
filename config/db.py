# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from typing import AsyncGenerator
# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import MetaData
from config import *
import databases


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# engine = create_async_engine(DATABASE_URL)
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

metadata = MetaData()
database = databases.Database(DATABASE_URL)
