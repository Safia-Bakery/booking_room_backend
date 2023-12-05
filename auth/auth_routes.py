from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from auth.settings import oauth, FRONTEND_URL
from starlette.responses import RedirectResponse, HTMLResponse, JSONResponse
from authlib.integrations.starlette_client import OAuthError

from schemas.schemas import TokenData
from utils.utils import CREDENTIALS_EXCEPTION, valid_email_from_db, get_db, create_token, get_current_user_email

auth_router = APIRouter(
    tags=['auth']
)


@auth_router.get('/', status_code=status.HTTP_200_OK)
def public(request: Request):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        return HTMLResponse(f'<p>Hello {name}!</p><a href=/logout>Logout</a>')
    return HTMLResponse('<body><a href="/login">Log In</a></body>')
    # return templates.TemplateResponse("auth.html", {"request": request})


@auth_router.get('/login')
async def login(request: Request):
    redirect_uri = FRONTEND_URL  # This creates the url for our /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


# @auth_router.get('/token_button')
# async def token(request: Request):
#     return HTMLResponse('''
#                 <script>
#                 function send(){
#                     var req = new XMLHttpRequest();
#                     req.onreadystatechange = function() {
#                         if (req.readyState === 4) {
#                             console.log(req.response);
#                             if (req.response["result"] === true) {
#                                 window.localStorage.setItem('jwt', req.response["access_token"]);
#                             }
#                         }
#                     }
#                     req.withCredentials = true;
#                     req.responseType = 'json';
#                     req.open("get", "/auth/token?"+window.location.search.substr(1), true);
#                     req.send("");
#
#                 }
#                 </script>
#                 <button onClick="send()">Get FastAPI JWT Token</button>
#             ''')


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
        print("SOMSODFDKISNNFS")
        # TODO: validate email in our database and generate JWT token
        jwt_token = create_token(access_token['userinfo']['email'])
        # TODO: return the JWT token to the user so it can make requests to our /api endpoint
        print("JWT TOKEN:\n", jwt_token)
        return JSONResponse({'result': True, 'access_token': jwt_token})
    raise CREDENTIALS_EXCEPTION


# @auth_router.get("/login", status_code=status.HTTP_200_OK)
# async def auth(request: Request):
#     redirect_uri = request.url_for('google-auth')  # This creates the url for the /auth endpoint
#     return await oauth.google.authorize_redirect(request, redirect_uri)
#
#
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

# @auth_router.post("/login", status_code=status.HTTP_200_OK)
# async def login(user: LoginUser, db: Session = Depends(get_db)):
#     user_id, token, token_type = await google_auth(user, db)
#     return {"user_id": user_id, "token": token}


# @auth_router.get("/", status_code=200)
# async def google_auth_render(request: Request):
#     return templates.TemplateResponse("auth.html", {"request": request})


@auth_router.get('/unprotected')
def test():
    return {'message': 'unprotected api_app endpoint'}


@auth_router.get('/protected')
def test2(current_email: str = Depends(get_current_user_email)):
    return {'message': 'protected api_app endpoint'}