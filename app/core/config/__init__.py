import os
from typing import Optional

class Config:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///hasbullita.db")
    ENABLE_PROFILING: bool = os.getenv("ENABLE_PROFILING", "true").lower() == "true"
    ENABLE_EXTENDED_LOGGING: bool = os.getenv("ENABLE_EXTENDED_LOGGING", "false").lower() == "true"

config = Config()