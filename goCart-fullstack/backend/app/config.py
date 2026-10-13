from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url: str = "sqlite:///./gocart.db"
    jwt_secret: str = "local-development-only-change-me"
    access_token_minutes: int = 120
    frontend_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
