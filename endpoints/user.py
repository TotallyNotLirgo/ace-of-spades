from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .security import protect, hash_value
from .schemas.user import LoginRequest
from .schemas.general import BasicResponse
from database.user import User

router = APIRouter(prefix="/users", tags=["User"])


@protect
@router.post("/login")
async def user_login(body: LoginRequest) -> BasicResponse:
    token, expiration = await User.login(body.email, hash_value(body.password))
    response = JSONResponse({"message": "OK"})
    response.set_cookie("token", token, secure=True, samesite="none")
    response.set_cookie("expiration", expiration, secure=True, samesite="none")
    return response
