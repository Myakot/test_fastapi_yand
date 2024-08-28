import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class User(BaseModel):
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def generate_token(user: User):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {
            "sub": user.username,
            "exp": int(datetime.now(timezone.utc).timestamp())
            + access_token_expires.total_seconds(),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        media_type="application/json",
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = User(username=username, email="")
    except JWTError:
        raise credentials_exception
    return user
