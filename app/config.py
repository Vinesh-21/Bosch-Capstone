from pydantic_settings import BaseSettings,SettingsConfigDict

_model_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore"
    )


class DatabaseSettings(BaseSettings):
    MYSQL_DB_USER:str
    MYSQL_DB_PASSWORD:str
    MYSQL_DB_HOST:str
    MYSQL_DB_PORT:int
    MYSQL_DB_NAME:str

    model_config =_model_config

    @property
    def get_MYSQL_URL(self):
        return f"mysql+aiomysql://{self.MYSQL_DB_USER}:{self.MYSQL_DB_PASSWORD}@{self.MYSQL_DB_HOST}:{self.MYSQL_DB_PORT}/{self.MYSQL_DB_NAME}"
    

databaseSettings =DatabaseSettings()