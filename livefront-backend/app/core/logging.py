from loguru import logger

logger.add(
    sink=lambda msg: print(msg, end=''),
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}\n",
    level="INFO"
)