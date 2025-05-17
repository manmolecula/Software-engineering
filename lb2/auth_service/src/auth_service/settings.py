from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "key"
    access_token_expiration: int = 1200
    debug_mode: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
