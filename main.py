import uvicorn
# from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, status, Request
from fastapi.staticfiles import StaticFiles

from routers import app_routes, admin_routes, auth_routes
from fastapi.middleware.cors import CORSMiddleware
# from config.config import SECRET_KEY


main_app = FastAPI(title="Book Meeting Room")

# main_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# main_app.mount(path='/app', app=app)
# main_app.mount(path='/auth', app=auth_app)
# main_app.mount(path='/admin', app=admin_app)


# if SECRET_KEY is None:
#     raise 'Missing SECRET_KEY'


main_app.include_router(app_routes.app_router)
main_app.include_router(auth_routes.auth_router)
main_app.include_router(admin_routes.admin_router)


ALLOWED_HOSTS = ["*"]
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


main_app.mount("/files", StaticFiles(directory="files"), name="files")


if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host="10.0.0.91",  # "10.0.2.59",
        port=8000,
        reload=True
    )
