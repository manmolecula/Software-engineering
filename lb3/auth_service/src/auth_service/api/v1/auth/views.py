from datetime import timedelta
from typing import Annotated

from fastapi import Response, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from .auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    create_new_user,
    delete_user,
    get_current_active_user,
    get_users,
)
from .models import Token, User, UserInDB

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@auth_router.post("/signup")
async def create_account(new_user: User, response: Response):
    await create_new_user(new_user)
    response.status_code = status.HTTP_201_CREATED
    logger.info(
        f'metric_name="registration" msg="created new user" user={new_user.username}'
    )
    return {"result": "created"}


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@auth_router.get("/users")
async def get_users_list(
    current_user: Annotated[str, Depends(get_current_active_user)],
):
    return await get_users()


@auth_router.delete("/users/{id}")
async def delete_user_view(
    id: int, current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    if current_user.role == "Admin":
        await delete_user(id)
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
