import os
from .admin_routes import admin_router
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse

# Create the auth app
# admin_app = FastAPI()
# admin_app.include_router(admin_router)
#
# # Set up the middleware to read the request session
# SECRET_KEY = os.environ.get('SECRET_KEY') or None
# if SECRET_KEY is None:
#     raise 'Missing SECRET_KEY'
#
# admin_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


