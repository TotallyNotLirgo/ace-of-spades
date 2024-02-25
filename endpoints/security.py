import logging
from fastapi import HTTPException
import traceback
from .schemas.general import APIError
from hashlib import sha256
from uuid import uuid4

logger = logging.getLogger(__name__)


def generate_token():
    return uuid4().urn.split(':')[-1]


def hash_value(value: str):
    return sha256(value.encode()).hexdigest()


def protect(callback):
    def protection(*args, **kwargs):
        try:
            return callback(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(e)
            logger.info(traceback.format_stack)
            raise APIError(500, "Unknown error occured")
    return protection
