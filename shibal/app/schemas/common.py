from pydantic import BaseModel


class ErrorScheme(BaseModel):
    error: str
