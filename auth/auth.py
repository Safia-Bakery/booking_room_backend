import os
from .auth_routes import auth_router
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError



# Create the auth app
auth_app = FastAPI()
auth_app.include_router(auth_router)

# Set up the middleware to read the request session
SECRET_KEY = os.environ.get('SECRET_KEY') or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'

auth_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
