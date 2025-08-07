from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/ping", tags=["health"])


@router.get("", response_class=PlainTextResponse)
def ping() -> str:
    """Health check endpoint"""
    return "pong"
