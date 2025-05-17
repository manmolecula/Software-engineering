from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug_mode: bool = True
    auth_url: str = "http://localhost:8000/api/v1/auth/token"
    secret_key: str = "key"

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_database: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
