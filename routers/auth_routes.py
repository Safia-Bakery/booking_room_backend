from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from routers.settings import oauth, FRONTEND_URL
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse
from authlib.integrations.starlette_client import OAuthError
from crud import crud
from schemas.schemas import CreateUser, Token, GoogleToken
from utils.utils import CREDENTIALS_EXCEPTION, valid_email_from_db, get_db, create_token, get_current_user_email, google_auth
import requests


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
templates = Jinja2Templates(directory="templates")


@auth_router.get("/", status_code=200)
async def google_auth_render(request: Request):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        return HTMLResponse(f'<p>Hello {name}!</p><a href=/logout>Logout</a>')
    return templates.TemplateResponse("home.html", {"request": request})


# @auth_router.get('/login')
# async def login(request: Request):
#     redirect_uri = FRONTEND_URL  # This creates the url for our /auth endpoint
#     return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_router.get('/token')
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        access_token = await oauth.google.authorize_access_token(request)
        print("TTTTTTTT")
        print("GOOGLE TOKEN:", access_token)
    except OAuthError:
        print("SSSSSS")
        raise CREDENTIALS_EXCEPTION
    # user_data = await oauth.google.parse_id_token(request, access_token)
    if valid_email_from_db(email=access_token['userinfo']['email'], db=db):
        print("User in DB")
        # TODO: validate email in our database and generate JWT token
        jwt_token = create_token(access_token['userinfo']['email'])
        # TODO: return the JWT token to the user so it can make requests to our /api endpoint
        print("JWT TOKEN:\n", jwt_token)
        return JSONResponse({'result': True, 'jwt_token': jwt_token})
    else:
        crud.create_user(db=db, form_data=access_token['userinfo'])
        jwt_token = create_token(access_token['userinfo']['email'])
        print("JWT TOKEN after creating user in DB:\n", jwt_token)
        return JSONResponse({'result': True, 'access_token': jwt_token})


@auth_router.get('/signup')
async def user_auth(user: CreateUser, token: GoogleToken, db: Session = Depends(get_db)):
    user_id, token = await google_auth(user, token, db)
    return {"user_id": user_id, "jwt_token": token}


# @auth_router.post('/user')
# async def user_create(user: LoginUser, db: Session = Depends(get_db)):
#     google_query = requests.get(f"https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token={user.token}")
#     if crud.add_user(db=db, form_data=google_query):
#         jwt_token = create_token(google_query['email'])


@auth_router.get("/login", status_code=status.HTTP_200_OK)
async def auth(db: Session = Depends(get_db)):
    # user_info = requests.get(f"https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token={google_token.token}")
    user_info = requests.get(f"https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=ya29.a0AfB_byBFLvuUN9qUbbC0A-vUXjnAgwe0grM2s2VyTKy1O5ZpnaicPRhmto5Xt9vVMpMv93oFybL3DoZ6TQ0y8k-5YpkFiwwUq-y-7XX2ZJJH5Oqs2uJAoYJpeDsiG-JF97zOFPTMOXGwko0j5DVSJQmGtzAFDZmVtlkaCgYKAXASARESFQHGX2MiEmwM5JG-D6SNudf3QRtKDg0170")
    user_dict = user_info.json()
    user_obj = crud.add_user(db=db, form_data=user_dict)
    if user_obj:
        jwt_token = create_token(user_dict['id'])
        return JSONResponse({'id': user_dict['id'], 'jwt_token': jwt_token})



# @auth_router.get('/google-auth', status_code=status.HTTP_200_OK)
# async def login(request: Request):
#     try:
#         access_token = await oauth.google.authorize_access_token(request)
#     except OAuthError:
#         return RedirectResponse(url='/')
#     user_data = await oauth.google.parse_id_token(request, access_token)
#     request.session['user'] = dict(user_data)
#     return RedirectResponse(url='/')


@auth_router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@auth_router.get('/unprotected')
def test():
    return {'message': 'unprotected api_app endpoint'}


@auth_router.get('/protected')
def test2(current_email: str = Depends(get_current_user_email)):
    return {'message': 'protected api_app endpoint'}