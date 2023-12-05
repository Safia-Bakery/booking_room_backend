import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, status, Request
from starlette.responses import HTMLResponse
from app.app_routes import app_router
from admin.admin_routes import admin_router
from auth.auth_routes import auth_router
from config.config import SECRET_KEY
from auth.auth import auth_app
from app.app import app
from admin.admin import admin_app
from fastapi.middleware.cors import CORSMiddleware


main_app = FastAPI(title="Book Meeting")

main_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

main_app.mount(path='/app', app=app)
main_app.mount(path='/auth', app=auth_app)
main_app.mount(path='/admin', app=admin_app)


if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'


main_app.include_router(app_router)
main_app.include_router(auth_router)
main_app.include_router(admin_router)


ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
