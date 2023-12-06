import os
from .app_routes import app_router
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware


# Create the auth app
# app = FastAPI()
# app.include_router(app_router)
#
# # Set up the middleware to read the request session
# SECRET_KEY = os.environ.get('SECRET_KEY') or None
# if SECRET_KEY is None:
#     raise 'Missing SECRET_KEY'
#
# app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

