import logging
import os

from pythonjsonlogger import jsonlogger

environment = os.getenv("ENV", "development")

formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)d %(message)s",
    json_ensure_ascii=False,
)

logger = logging.getLogger("country_agent")
logger.setLevel(logging.INFO)

if environment == "production":
    handler = logging.StreamHandler()
else:
    try:
        handler = logging.FileHandler(filename="logs.log")
    except OSError:
        handler = logging.StreamHandler()

handler.setFormatter(formatter)
logger.addHandler(handler)
