from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from auth import hash_password, verify_password, create_access_token
from database import load_users
from models import UserCreate, UserLogin, UserUpdate, UserOut
from redis_manager import RedisManager

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
redis_manager = RedisManager()

def register_user(user: UserCreate, role: str):
    if redis_manager.get_user(user.email):
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    new_user = {
        "id": len(load_users()) + 1,
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "role": role,
    }

    redis_manager.set_user(new_user)
    return {"message": "Вы зарегистрированы"}

@router.post("/Api/v1/user/create", tags=["Регистрация пользователя"])
def register_regular_user(user: UserCreate):
    return register_user(user, role="user")

@router.post("/Api/v1/login", tags=["Авторизация пользователя (получение токена)"])
def login_user(user: UserLogin):
    db_user = redis_manager.get_user(user.email)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    token = create_access_token(db_user["email"], db_user["role"], db_user["id"])
    return {"access_token": token, "token_type": "Bearer"}

@router.delete("/Api/v1/user/delete", tags=["Пользователь"])
def delete_user(email: str):
    if not redis_manager.delete_user(email):
        raise HTTPException(status_code=404, detail="Пользователь не существует")
    return {"message": "Пользователь удален"}

@router.put("/Api/v1/user/update", tags=["Пользователь"])
def update_user(user: UserUpdate):
    db_user = redis_manager.get_user(str(user.email))
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не cуществует")

    if user.new_name:
        db_user["name"] = user.new_name
    if user.new_email:
        db_user["email"] = user.new_email
    if user.new_password:
        db_user["password"] = hash_password(user.new_password)

    redis_manager.set_user(db_user)
    return {"message": "Данные пользователя обновлены"}

@router.get("/Api/v1/user/get_all", tags=["Пользователь"])
def get_all_users():
    users = redis_manager.get_all_users()
    if not users:
        raise HTTPException(status_code=404, detail="Нет пользователей")
    return {"users": users}