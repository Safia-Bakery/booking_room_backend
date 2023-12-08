from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status
import os
from config.config import SECRET_KEY, ALGORITHM, GOOGLE_CLIENT_ID, ACCESS_TOKEN_EXPIRE_MINUTES, EMAIL_PASSWORD, EMAIL_USERNAME
from config.db import SessionLocal
from crud import crud
from schemas.schemas import TokenData, GoogleToken, GetUser, CreateUser

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helper to read numbers using var envs
def cast_to_number(id):
    temp = os.environ.get(id)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None


SECRET_KEY = SECRET_KEY or None

if SECRET_KEY is None:
    raise 'Missing API_SECRET_KEY env var.'

ALGORITHM = ALGORITHM or 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES) or 15
access_token_jwt_subject = "access"

# Token url (We should later create a token url that accepts just a user and a password to use it with Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
#     return encoded_jwt


# Create token internal function
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})  # "sub": access_token_jwt_subject
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Create token for an email
# def create_token(email):
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={'sub': email}, expires_delta=access_token_expires)
#     return access_token

# Create token for user id
def create_token(email: str):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': email}, expires_delta=access_token_expires)
    return access_token


def valid_email_from_db(email, db: Session = Depends(get_db)):
    return crud.check_email(db=db, email=email)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expire_date: int = payload.get('exp')
        email: str = payload.get('sub')
        if email is None:
            raise CREDENTIALS_EXCEPTION
        if datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token is expired',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        token_data = TokenData(email=email)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = crud.check_email(db=db, email=email)
    if user is None:
        raise CREDENTIALS_EXCEPTION

    return user


async def email_sender(receivers, organizer, room, meeting_name, start_time, end_time):
    subject = "Organized meeting"
    body = (f"You were invited to meeting {meeting_name} organized by {organizer}.\n"
            f"Meeting get place in {room} at {start_time} and continue until {end_time}")
    sender_email = str(EMAIL_USERNAME)
    receiver_email = receivers
    password = str(EMAIL_PASSWORD)

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receivers)
    message["Subject"] = subject
    # message["Bcc"] = receiver_email[1: len(receivers)]  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Convert message to string
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        print("Messages were sent successfully!")



# def verify_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(email=email)
#     except JWTError:
#         raise credentials_exception
#
#
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     return verify_token(token=token, credentials_exception=credentials_exception)


# async def get_current_active_user(
#         current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# async def google_auth(user: CreateUser, token: GoogleToken, db: Session = Depends(get_db)):
#     print("########### Token ##########\n", user.token)
#     try:
#         id_info = id_token.verify_oauth2_token(token.token, requests.Request(), GOOGLE_CLIENT_ID)
#         print("There ERROR")
#     except ValueError:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bad code")
#     created_user = crud.get_or_create_user(db=db, form_data=user)
#     if not created_user:
#         raise HTTPException(status_code=status.HTTP_302_FOUND, detail='User with the email already exists!')
#     # access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
#     # access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
#     # return {"user_id": created_user.id, "access_token": jsonable_encoder(access_token), "token_type": "GoogleOAuth2"}
#     access_token = create_token(created_user.id)
#     return created_user.id, access_token
