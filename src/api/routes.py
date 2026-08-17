"""FastAPI route declarations and endpoints."""

from fastapi import APIRouter
from src.schemas.common import APIResponse

router = APIRouter()


@router.get("/health", response_model=APIResponse[dict])
async def health_check():
    """Health check endpoint."""
    return APIResponse(data={"status": "healthy"})
