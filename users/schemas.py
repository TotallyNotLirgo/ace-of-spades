from pydantic import BaseModel, Field, field_validator
from .validators import validate_password, validate_username, validate_email
from fastapi import HTTPException


class UserLoginRequest(BaseModel):
    username_or_email: str = Field(
        description="The username or email of the user", examples=["user"]
    )

    password: str = Field(
        description="The password of the user", examples=["Password123!"]
    )


class UserCreateRequest(UserLoginRequest):
    username: str = Field(
        description="The username of the user", examples=["user"]
    )
    password: str = Field(
        description="The password of the user", examples=["Password123!"]
    )
    email: str = Field(
        description="The email of the user", examples=["user@email.com"]
    )

    @field_validator("username")
    def validate_username(cls, v: str) -> str:
        try:
            return validate_username(v)
        except ValueError as e:
            raise HTTPException(422, str(e))

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        try:
            return validate_password(v)
        except ValueError as e:
            raise HTTPException(422, str(e))

    @field_validator("email")
    def validate_email(cls, v: str) -> str:
        try:
            return validate_email(v)
        except ValueError as e:
            raise HTTPException(422, str(e))


class UserReadResponse(BaseModel):
    id: int = Field(description="The id of the user", examples=[1])
    username: str = Field(
        description="The username of the user", examples=["user"]
    )
    role: str = Field(description="The role of the user", examples=["user"])
    profile_picture: str | None = Field(
        None,
        description="The profile picture of the user",
        examples=["user.jpg"]
    )


class UserUpdateRequest(BaseModel):
    username: str | None = Field(
        None, description="The username of the user", examples=["user"]
    )
    password: str | None = Field(
        None, description="The password of the user", examples=["Password123!"]
    )
    email: str | None = Field(
        None, description="The email of the user", examples=["user@email.com"]
    )
    profile_picture: str | None = Field(
        None,
        description="The profile picture of the user",
        examples=["user.jpg"]
    )
    role: str | None = Field(
        None, description="The role of the user", examples=["admin"]
    )

    @field_validator("username")
    def validate_username(cls, v: str | None) -> str | None:
        if v is None:
            return v
        try:
            return validate_username(v)
        except ValueError as e:
            raise HTTPException(422, str(e))

    @field_validator("password")
    def validate_password(cls, v: str | None) -> str | None:
        if v is None:
            return v
        try:
            return validate_password(v)
        except ValueError as e:
            raise HTTPException(422, str(e))

    @field_validator("email")
    def validate_email(cls, v: str | None) -> str | None:
        if v is None:
            return v
        try:
            return validate_email(v)
        except ValueError as e:
            raise HTTPException(422, str(e))


class UserAuth(BaseModel):
    id: int = Field(description="The id of the user", examples=[1])
    role: str = Field(description="The role of the user", examples=["user"])
