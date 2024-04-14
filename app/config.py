from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    # model_config = SettingsConfigDict(env_file='.env')
    
    class Config:
        env_file = ".env"
    

settings = Settings(_env_file=".env")


    
# class Settings(BaseSettings):
#     # list of all the env variables
#     # can't leave a field missing because then it misses the whole point
#     database_password: str = "localhost"
#     database_username: str = "postgres"
#     secret_key: str = "23456789wadsfwrt4354y6udcgfnxb"
    