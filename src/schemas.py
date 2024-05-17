from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseSchema(BaseModel):
    code: int | None = None
    message: str | None = None
    data: list | dict


class ValidationResponseSchema(BaseModel):
    code: int | None = None
    message: list[T] | None = None
    data: list | None = []
