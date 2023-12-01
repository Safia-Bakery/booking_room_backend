from typing import List

from fastapi import FastAPI
from routers.app_routes import app_router
from routers.auth_routes import auth_router
from routers.admin_routes import admin_router


app = FastAPI(
    title="Book Meeting"
)


# @AuthJWT.load_config
# def get_config():
#     return Settings()


app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(app_router)
