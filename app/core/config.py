from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All configuration is read from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "Romp"
    debug: bool = False
    version: str = "0.1.0"

    # Database
    database_url: str = "postgresql+asyncpg://romp:romp@localhost:5432/romp"
    test_database_url: str = "postgresql+asyncpg://romp:romp@localhost:5432/romp_test"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # AWS
    aws_region: str = "us-west-2"
    s3_bucket_name: str = "romp-images"


settings = Settings()
