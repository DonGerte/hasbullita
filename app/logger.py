from loguru import logger
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logger.add("logs/app.log", rotation="10 MB", level="INFO")