import os

import jwt
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from datetime import datetime, timezone
from jwt.exceptions import InvalidKeyError
from passlib.context import CryptContext

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("JWT_SECREET_KEY", "6d0f458775db7fb3bf3ac434477f3f689eee5f83a37aab93e337657afc5f0c2e")
YH_PASSWORD = os.getenv("YH_PASSWORD", "password")

USERS_DB = []
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTToken(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    active: bool = True
    id: int


class UserRequest(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)
    email: str = Field(min_length=4)

    model_config = {
            "json_schema_extra": {
                "example": {
                    "username": "username",
                    "password": "password",
                    "email": "yfaney@gmail.com"
                    }
                }
            }


USERS_DB = [
    User(username="yfaney", hashed_password=bcrypt_context.hash(YH_PASSWORD), email="yfaney@gmail.com", id=1)
]

def set_user_id():
    print("Set id")
    if len(USERS_DB) > 0:
        return USERS_DB[-1].id + 1
    else:
        return 1


def get_user_from_db(username):
    for u in USERS_DB:
        if username == u.username:
            return u


async def get_current_user(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="login"))]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="U/name missing.")
        expires = payload.get("exp")
        if datetime.now(timezone.utc) > datetime.fromtimestamp(expires, timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired.")
    except InvalidKeyError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token error.")

    user = get_user_from_db(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="U/name not found")
    return user

def register_new_user(new_user):
    """ Register new user and add to the database """
    if get_user_from_db(new_user.username) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username exists")
    new_user = User(
            username=new_user.username,
            hashed_password=bcrypt_context.hash(new_user.password),
            email=new_user.email,
            id=set_user_id()
            )
    USERS_DB.append(new_user)
    return new_user


def update_user(current_user, updated_user):
    """ Update my user information """
    print(f"Update user: {updated_user}")
    if get_user_from_db(updated_user.username) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username exists")
    current_user.username = updated_user.username
    current_user.hashed_password = bcrypt_context.hash(updated_user.password)
    current_user.email = updated_user.email
    return updated_user


# Delete
def delete_user(username):
    for i in range(len(USERS_DB)):
        if USERS_DB[i].username == username:
            USERS_DB.pop(i)
            break


def authenticate_user(username, password):
    """ Validate username;Validate password """

    #1.1 Validate username
    existing_user = None
    for u in USERS_DB:
        if u.username == username:
            existing_user = u
            break
    if existing_user is None:
        return None

    #1.2 Validate password
    if not bcrypt_context.verify(password, existing_user.hashed_password):
        return None

    return u
  