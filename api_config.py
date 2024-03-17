import traceback
from logging import getLogger

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from general.config import get_config

logger = getLogger(__name__)
config = get_config()


API_INFO = {
    "title": "Ace of Spades API",
    "description": "API for Ace of Spades",
    "version": "0.0.1",
    "openapi_url": "/openapi.json",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
}

CORS_CONFIG = {
    "middleware_class": CORSMiddleware,
    "allow_origins": [config.FRONTEND_URL],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}


class ExceptionHandlers:
    @classmethod
    async def http(cls, request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse({"error": exc.detail}, exc.status_code)

    @classmethod
    async def validation(
        cls, request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.error(exc)
        return JSONResponse({"error": "Unprocessable Entity"}, 422)

    @classmethod
    async def unknown(cls, request: Request, exc: Exception) -> JSONResponse:
        logger.error(exc)
        logger.debug(traceback.format_exc())
        return JSONResponse({"error": "Internal Server Error"}, 500)
