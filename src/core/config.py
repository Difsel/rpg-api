from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    debug: bool
    database_url: str
    redis_url: str

    postgres_user: str
    postgres_password: str
    postgres_db: str

    jwt_secret: str
    jwt_algorithm: str
    jwt_expire_min: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
