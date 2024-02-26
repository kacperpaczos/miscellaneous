from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    version: str = "0.0.5"
    debug: bool = True

# load and parse settings
settings = Settings()

# access variables
version = settings.version
debug = settings.debug
