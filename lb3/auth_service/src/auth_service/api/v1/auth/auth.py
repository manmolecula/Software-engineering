from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger
from passlib.context import CryptContext

from ....external.postgres.utils import (
    create_user,
    delete_user_from_db,
    get_user_from_db,
    get_users_from_db,
)
from ....settings import settings
from .models import TokenData, User, UserInDB

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expiration


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await get_user_from_db(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_new_user(new_user: User):
    if new_user.role == "Admin":
        raise HTTPException(status_code=400, detail="Cant register as admin")
    user = await get_user_from_db(new_user.username)
    if user:
        raise HTTPException(
            detail="User already exists", status_code=status.HTTP_409_CONFLICT
        )
    else:
        try:
            await create_user(
                UserInDB(
                    password=new_user.password,
                    initials=new_user.initials,
                    role=new_user.role,
                    username=new_user.username,
                    hashed_password=get_password_hash(new_user.password),
                )
            )  # type: ignore
        except Exception as e:
            logger.error(f"Error during execution of create_user: {e}")
            raise HTTPException(
                detail="Database issue", status_code=status.HTTP_502_BAD_GATEWAY
            )


async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # type: ignore
        role: str = payload.get("role")  # type: ignore
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    user = await get_user_from_db(username=token_data.username)  # type: ignore
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_users() -> list[UserInDB]:
    return await get_users_from_db()


async def delete_user(id: int):
    await delete_user_from_db(id)
