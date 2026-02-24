from pydantic import BaseModel
from pydantic import Field
from starlette.responses import JSONResponse


class ResponseError(BaseModel):
    code: str
    message: str
    details: list[str] = Field(default_factory=list)


def error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    details: list[str] | None = None,
) -> JSONResponse:
    payload = ResponseError(code=code, message=message, details=details or [])
    return JSONResponse(status_code=status_code, content=payload.model_dump())