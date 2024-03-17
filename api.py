from logging import getLogger

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from api_config import API_INFO, CORS_CONFIG, ExceptionHandlers
from general.config import get_config
from general.logger import init_logger
import users.endpoints as users

config = get_config()
init_logger(config.LOG_LEVEL, config.LOG_FILE, config.CONSOLE_ENABLED)
logger = getLogger(__name__)

logger.info("Starting Ace of Spades API")
logger.info(
    f"Documentation: https://{config.API_HOST}:{config.API_PORT}"
    f"{API_INFO['docs_url']}"
)
app = FastAPI(**API_INFO)

app.add_middleware(**CORS_CONFIG)
app.exception_handler(HTTPException)(ExceptionHandlers.http)
app.exception_handler(404)(ExceptionHandlers.http)
app.exception_handler(403)(ExceptionHandlers.http)
app.exception_handler(401)(ExceptionHandlers.http)
app.exception_handler(RequestValidationError)(ExceptionHandlers.validation)
app.exception_handler(Exception)(ExceptionHandlers.unknown)

app.include_router(users.router)
