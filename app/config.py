from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    redis_url: str = "redis://localhost:6379"
    core_secret: str = "test_secret"
    telegram_admin_bot_token: str = "test_token"
    telegram_whisper_bot_token: str = "test_token"
    telegram_music_bot_token: str = "test_token"
    
    # BPS configurable thresholds
    bps_warning_threshold: int = 5
    bps_ban_threshold: int = 10
    bps_soft_warn_threshold: int = 3
    bps_conflict_risk_threshold: float = 0.5
    bps_spam_risk_threshold: float = 0.7

    class Config:
        env_file = ".env"

settings = Settings()