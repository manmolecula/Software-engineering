from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug_mode: bool = True
    auth_url: str = "http://localhost:8000/api/v1/auth/token"
    secret_key: str = "key"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
