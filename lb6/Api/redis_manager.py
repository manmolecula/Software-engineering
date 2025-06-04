import json
from typing import List, Dict, Optional
import redis
from database import load_users, save_users, find_user_by_email, delete_user_by_email


class RedisManager:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def _get_user_key(self, email: str) -> str:
        """Генерирует ключ для хранения пользователя в Redis"""
        return f"user:{email}"

    def _get_all_users_key(self) -> str:
        """Генерирует ключ для хранения списка всех пользователей"""
        return "users:all"

    def get_user(self, email: str) -> Optional[Dict]:
        """Получает пользователя из кеша или БД (Cache-Aside)"""
        user_data = self.redis.get(self._get_user_key(email))
        if user_data:
            return json.loads(user_data)

        db_user = find_user_by_email(email)
        if db_user:
            self.set_user(db_user)
            return db_user

        return None

    def get_all_users(self) -> List[Dict]:
        """Получает всех пользователей из кеша или БД (Cache-Aside)"""
        users_data = self.redis.get(self._get_all_users_key())
        if users_data:
            return json.loads(users_data)

        db_users = load_users()
        if db_users:
            self.redis.setex(
                self._get_all_users_key(),
                3600,  # TTL 1 час
                json.dumps(db_users)
            )
            return db_users

        return []

    def set_user(self, user_data: Dict) -> bool:
        """Сохраняет пользователя в кеш и БД (Write-Through)"""
        email = user_data.get('email')
        if not email:
            return False

        users = load_users()
        existing_user = next((u for u in users if u['email'] == email), None)

        if existing_user:
            users = [u if u['email'] != email else user_data for u in users]
        else:
            users.append(user_data)

        save_users(users)

        self.redis.setex(
            self._get_user_key(email),
            3600,  # TTL 1 час
            json.dumps(user_data)
        )

        self.redis.delete(self._get_all_users_key())

        return True

    def delete_user(self, email: str) -> bool:
        """Удаляет пользователя из кеша и БД (Write-Through)"""
        result = delete_user_by_email(email)
        if not result:
            return False

        self.redis.delete(self._get_user_key(email))
        self.redis.delete(self._get_all_users_key())

        return True

    def refresh_cache(self) -> None:
        """Обновляет весь кеш из БД"""
        users = load_users()
        if users:
            self.redis.setex(
                self._get_all_users_key(),
                3600,
                json.dumps(users)
            )

            for user in users:
                self.redis.setex(
                    self._get_user_key(user['email']),
                    3600,
                    json.dumps(user)
                )

    def clear_cache(self) -> None:
        """Очищает весь кеш"""
        keys = self.redis.keys("user:*") + self.redis.keys("users:*")
        if keys:
            self.redis.delete(*keys)