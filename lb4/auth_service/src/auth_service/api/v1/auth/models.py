from typing import Literal, Union

from pydantic import BaseModel


class User(BaseModel):
    initials: str
    username: str
    role: Literal["Guest", "User", "Admin"] = "User"
    disabled: Union[bool, None] = False
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    role: Union[str, None] = None


class UserInDB(User):
    id: int = -1
    hashed_password: str
