from datetime import date
from datetime import datetime
from datetime import timezone
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import Response
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import model_validator
from pydantic_core import ValidationError
from starlette.responses import JSONResponse

from src.app.api.errors import ResponseError
from src.app.api.errors import error_response
from src.app.api.dependencies import get_user_repository
from src.modules.users.application.create_user import CreateUserUseCase
from src.modules.users.application.delete_user import DeleteUserUseCase
from src.modules.users.application.get_user import GetUserByIdUseCase
from src.modules.users.application.get_user import GetUsersUseCase
from src.modules.users.application.update_user import UpdateUserUseCase
from src.modules.users.domain.exceptions import DuplicateUserEmailError
from src.modules.users.domain.exceptions import InvalidUserPatchError
from src.modules.users.domain.exceptions import UserNotFoundError
from src.modules.users.domain.models.user import User
from src.modules.users.domain.models.user import UserPatchData
from src.modules.users.domain.models.user import UserRole
from src.modules.users.domain.repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


class UserPost(BaseModel):
    name: str
    email: EmailStr
    birthDate: date


class UserPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    email: EmailStr | None = None
    birthDate: int | None = None

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "UserPatch":
        if self.name is None and self.email is None and self.birthDate is None:
            raise ValueError("At least one field must be provided")
        return self


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    birthDate: date
    role: UserRole


class UsersResponse(BaseModel):
    data: list[UserResponse]


def _to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        birthDate=user.birth_date,
        role=user.role,
    )


def _epoch_ms_to_date(value: int) -> date:
    if value < 0:
        raise InvalidUserPatchError("birthDate must be a positive epoch in milliseconds")
    try:
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc).date()
    except (ValueError, OSError, OverflowError) as error:
        raise InvalidUserPatchError("birthDate is not a valid epoch in milliseconds") from error


@router.get("", response_model=UsersResponse, operation_id="getUsers")
async def get_users(
    filter: str | None = Query(default=None),
    repository: UserRepository = Depends(get_user_repository),
) -> UsersResponse:
    users = await GetUsersUseCase(repository).execute(filter_by_name=filter)
    return UsersResponse(data=[_to_response(user) for user in users])


@router.post("", response_model=UserResponse, status_code=201, operation_id="createUser")
async def create_user(
    payload: UserPost,
    response: Response,
    repository: UserRepository = Depends(get_user_repository),
) -> UserResponse | JSONResponse:
    try:
        user = await CreateUserUseCase(repository).execute(
            name=payload.name,
            email=str(payload.email),
            birth_date=payload.birthDate,
        )
    except DuplicateUserEmailError:
        return error_response(
            status_code=400,
            code="INVALID_EMAIL",
            message="Email already exists",
        )
    response.headers["Location"] = f"/v1/users/{user.id}"
    return _to_response(user)


@router.get(
    "/{id}",
    response_model=UserResponse,
    operation_id="getUserById",
    responses={404: {"model": ResponseError}},
)
async def get_user_by_id(
    id: UUID,
    repository: UserRepository = Depends(get_user_repository),
) -> UserResponse | JSONResponse:
    try:
        user = await GetUserByIdUseCase(repository).execute(id)
    except UserNotFoundError:
        return error_response(
            status_code=404,
            code="NOT_FOUND",
            message="The requested resource does not exist",
        )
    return _to_response(user)


@router.patch(
    "/{id}",
    response_model=UserResponse,
    operation_id="patchUser",
    responses={400: {"model": ResponseError}, 404: {"model": ResponseError}},
)
async def patch_user(
    id: UUID,
    payload: UserPatch,
    repository: UserRepository = Depends(get_user_repository),
) -> UserResponse | JSONResponse:
    try:
        patch_data = UserPatchData(
            name=payload.name,
            email=str(payload.email) if payload.email is not None else None,
            birth_date=_epoch_ms_to_date(payload.birthDate)
            if payload.birthDate is not None
            else None,
        )
        user = await UpdateUserUseCase(repository).execute(id, patch_data)
    except (InvalidUserPatchError, ValidationError) as error:
        return error_response(
            status_code=400,
            code="VALIDATION_ERROR",
            message=str(error),
        )
    except DuplicateUserEmailError:
        return error_response(
            status_code=400,
            code="INVALID_EMAIL",
            message="Email already exists",
        )
    except UserNotFoundError:
        return error_response(
            status_code=404,
            code="NOT_FOUND",
            message="The requested resource does not exist",
        )
    return _to_response(user)


@router.delete(
    "/{id}",
    status_code=204,
    operation_id="deleteUser",
    responses={404: {"model": ResponseError}},
)
async def delete_user(
    id: UUID,
    repository: UserRepository = Depends(get_user_repository),
) -> Response:
    try:
        await DeleteUserUseCase(repository).execute(id)
    except UserNotFoundError:
        return error_response(
            status_code=404,
            code="NOT_FOUND",
            message="The requested resource does not exist",
        )
    return Response(status_code=204)