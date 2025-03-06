from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "0197542fdac221d75016a3381e21b5592e33efc4adcef09fa9a86d7235456170"  
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
