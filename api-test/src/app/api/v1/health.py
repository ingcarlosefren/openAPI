from fastapi import APIRouter
from fastapi import Response

router = APIRouter(tags=["Health"])


@router.get("/health", status_code=200)
async def health_check() -> Response:
    return Response(status_code=200)