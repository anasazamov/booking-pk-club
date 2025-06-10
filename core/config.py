import os
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings


def get_env_flag(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in ("1", "true", "yes")


class Settings(BaseSettings):
    # Environment
    ENV: str = Field("development", env="ENV")
    DEBUG: bool = Field(default=False)

    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # Redis / Celery
    REDIS_URL: AnyUrl = Field(..., env="REDIS_URL")
    CELERY_BROKER_URL: AnyUrl = Field(..., env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: AnyUrl = Field(..., env="CELERY_RESULT_BACKEND")

    # JWT
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 7, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # OTP
    OTP_EXPIRE_MINUTES: int = Field(5, env="OTP_EXPIRE_MINUTES")

    # iCafe integration
    ICAFE_API_URL: AnyUrl = Field(..., env="ICAFE_API_URL")
    ICAFE_API_KEY: str = Field(..., env="ICAFE_API_KEY")
    ICAFE_API_SECRET: str = Field(..., env="ICAFE_API_SECRET")

    # Internationalization
    LANGUAGES: list[str] = Field(["ru", "uz", "en"], env="LANGUAGES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
