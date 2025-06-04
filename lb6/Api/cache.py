import json
from typing import Optional, List
import redis
from database import User
from models import UserOut

class RedisCache:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.cache_ttl = 3600  # Время жизни кеша в секундах (1 час)

    def _user_to_dict(self, user: User) -> dict:
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role
        }

    def _dict_to_user(self, data: dict) -> UserOut:
        return UserOut(**data)

    def get_user(self, user_id: int) -> Optional[UserOut]:
        """Получить пользователя из кеша"""
        data = self.redis_client.get(f"user:{user_id}")
        if data:
            return self._dict_to_user(json.loads(data))
        return None

    def get_all_users(self) -> Optional[List[UserOut]]:
        """Получить всех пользователей из кеша"""
        data = self.redis_client.get("users:all")
        if data:
            return [self._dict_to_user(user_data) for user_data in json.loads(data)]
        return None

    def set_user(self, user: User) -> None:
        """Сохранить пользователя в кеш"""
        user_data = self._user_to_dict(user)
        self.redis_client.setex(
            f"user:{user.id}",
            self.cache_ttl,
            json.dumps(user_data)
        )

    def set_all_users(self, users: List[User]) -> None:
        """Сохранить всех пользователей в кеш"""
        users_data = [self._user_to_dict(user) for user in users]
        self.redis_client.setex(
            "users:all",
            self.cache_ttl,
            json.dumps(users_data)
        )

    def delete_user(self, user_id: int) -> None:
        """Удалить пользователя из кеша"""
        self.redis_client.delete(f"user:{user_id}")
        self.redis_client.delete("users:all")  # Инвалидируем кеш всех пользователей

    def clear_cache(self) -> None:
        """Очистить весь кеш"""
        self.redis_client.flushdb()