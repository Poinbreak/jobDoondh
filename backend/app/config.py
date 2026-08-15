from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str = ""
    supabase_service_key: str = ""
    anthropic_api_key: str = ""
    adzuna_app_id: str = ""
    adzuna_app_key: str = ""
    daily_pitch_limit: int = 5
    scrape_interval_hours: int = 6

    class Config:
        env_file = ".env"

settings = Settings()
