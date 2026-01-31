from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_bot_token: str
    database_url: str = "sqlite:///./hasbullita.db"
    enable_profiling: bool = True
    enable_extended_logging: bool = False

    # External API keys
    openweather_api_key: str = ""
    newsapi_key: str = ""

    # Optional APIs for future features
    spotify_client_id: str = ""
    spotify_client_secret: str = ""
    youtube_api_key: str = ""
    google_calendar_api_key: str = ""

    # BPS configurable thresholds
    bps_warning_threshold: int = 5
    bps_ban_threshold: int = 10
    bps_soft_warn_threshold: int = 3
    bps_conflict_risk_threshold: float = 0.5
    bps_spam_risk_threshold: float = 0.7

    class Config:
        env_file = ".env"


settings = Settings()
