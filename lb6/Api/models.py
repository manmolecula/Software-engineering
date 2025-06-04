from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., example="admin")
    email: EmailStr = Field(..., example="admin@admin.com")
    password: str = Field(..., example="secret")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="admin@admin.com")
    password: str = Field(..., example="secret")


class UserUpdate(BaseModel):
    email: EmailStr = Field(..., example="admin@admin.ru")
    new_name: str = Field(default=None, example="admin1")
    new_email: EmailStr = Field(default=None, example="admin1@admin.com")
    new_password: str = Field(default=None, example="secret1")

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True