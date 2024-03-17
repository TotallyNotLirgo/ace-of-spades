from pydantic import BaseModel, Field


class BasicResponse(BaseModel):
    message: str = Field("Success!", description="The message of the response")


class ErrorResponse(BaseModel):
    error: str = Field("Error", description="The error message")
