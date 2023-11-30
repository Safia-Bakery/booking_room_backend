from typing import List

from fastapi import FastAPI
from routers.app_routes import app_router
from routers.auth_routes import auth_router
from fastapi_jwt_auth import AuthJWT
from schemas.schemas import Settings


app = FastAPI(
    title="Book Meeting"
)


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(app_router)
app.include_router(auth_router)
