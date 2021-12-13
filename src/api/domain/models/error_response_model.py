from pydantic import BaseModel

class ErrorResponseModel(BaseModel):
    error: str
    code: int
    message: str
