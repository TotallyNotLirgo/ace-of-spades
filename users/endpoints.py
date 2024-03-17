from fastapi import APIRouter, Cookie, HTTPException
from fastapi.responses import JSONResponse
from .schemas import (
    UserLoginRequest,
    UserCreateRequest,
    UserReadResponse,
    UserUpdateRequest,
)
from general.schemas import BasicResponse, ErrorResponse
from .methods import User
from typing import Annotated

router = APIRouter(prefix="/users", tags=["User"])


@router.post(
    "/login",
    description="Login a user",
    responses={
        200: {"model": BasicResponse},
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    }
)
async def user_login(user: UserLoginRequest) -> BasicResponse:
    """
    Login a user
    Args:
        user (UserLoginRequest): The user to login
    Returns:
        BasicResponse: The response
    """
    token = await User.login(user)
    response = JSONResponse({"message": "Login successful"})
    response.set_cookie("token", token, secure=True, samesite="none")
    return response


@router.post(
    "/register",
    description="Create a user",
    responses={
        200: {"model": BasicResponse},
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    }
)
async def user_create(user: UserCreateRequest) -> BasicResponse:
    """
    Create a user
    Args:
        user (UserCreateRequest): The user to create
    Returns:
        BasicResponse: The response
    """
    await User.create(user)
    return {"message": "User created"}


@router.post(
    "/confirm",
    description="Confirm a user",
    responses={
        200: {"model": BasicResponse},
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    }
)
async def user_confirm(token: str) -> BasicResponse:
    """
    Confirm a user
    Args:
        token (str): The token to confirm
    Returns:
        BasicResponse: The response
    """
    auth = User.authorize(token)
    if auth.role != "new_user":
        raise HTTPException(409, "User already confirmed")
    await User.confirm(token)
    return {"message": "User confirmed"}


@router.get(
    "/",
    description="Search for users",
    responses={
        200: {"model": list[UserReadResponse]},
        422: {"model": ErrorResponse},
    }
)
async def user_search(query: str = "") -> list[UserReadResponse]:
    """
    Search for users
    Args:
        query (str): The query to search for
    Returns:
        list[UserReadResponse]: The users
    """
    return await User.search(query)


@router.get(
    "/{user_id}",
    description="Read a user",
    responses={
        200: {"model": UserReadResponse},
        404: {"model": ErrorResponse},
    }
)
async def user_read(user_id: int) -> UserReadResponse:
    """
    Retrieve user information
    Args:
        user_id (int): The id of the user
    Returns:
        UserReadResponse: The user
    """
    return await User.read(user_id)


@router.patch(
    "/{user_id}",
    description="Update a user",
    responses={
        200: {"model": BasicResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    }
)
async def user_update(
    user_id: int, user: UserUpdateRequest, token: Annotated[str, Cookie] = ""
) -> BasicResponse:
    """
    Update a user
    Args:
        user_id (int): The id of the user
        user (UserUpdateRequest): The user data to update
    Returns:
        BasicResponse: The response
    """
    auth = await User.authorize(token)
    if auth.role != "admin" and auth.id != user_id:
        raise HTTPException(403, "Unauthorized")
    await User.update(user_id, user)
    return {"message": "User updated"}


@router.delete(
    "/{user_id}",
    description="Delete a user",
    responses={
        200: {"model": BasicResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    }
)
async def user_delete(
    user_id: int, token: Annotated[str, Cookie] = ""
) -> BasicResponse:
    """
    Delete a user
    Args:
        user_id (int): The id of the user
    Returns:
        BasicResponse: The response
    """
    auth = await User.authorize(token)
    if auth.role != "admin" and auth.id != user_id:
        raise HTTPException(403, "Unauthorized")
    await User.delete(user_id)
    return {"message": "User deleted"}
