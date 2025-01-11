import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE_PATH = pathlib.Path(__file__).parents[2].joinpath(".env")


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    rabbitmq_host: str
    rabbitmq_port: str
    rabbitmq_web_port: str

    redis_host: str
    redis_port: str

    jwt_secret_key: str

    auth_prefix: str = "/auth"
    strategies_prefix: str = "/strategies"

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, env_file_encoding="utf-8", extra="ignore")

    @property
    def sqlalchemy__database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
