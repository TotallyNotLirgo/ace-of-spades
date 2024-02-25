from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from general.logger import init_logger
from endpoints.schemas.general import APIError
from general.config import get_config
from endpoints import user

# ________ INITIALIZATION ________ #

init_logger()
logger = logging.getLogger(__name__)

app = FastAPI()
config = get_config()
logger.info("Starting API")

app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(APIError)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


@app.exception_handler(404)
async def exception_404_handler(request: Request, exc: HTTPException):
    if exc.detail == 'Not Found':
        return JSONResponse(
            status_code=exc.status_code,
            content={'error': 'Not Found'},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


@app.exception_handler(403)
async def exception_403_handler(request: Request, exc: HTTPException):
    try:
        exc.detail['error']
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
        )
    except (KeyError, TypeError):
        return JSONResponse(
            status_code=exc.status_code,
            content={'error': 'No authorization header'},
        )


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Unprocessable Entity"}
    )
