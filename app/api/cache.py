from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.cache_service import CacheService

router = APIRouter(prefix="/cache", tags=["cache"])

# Initialize cache service
cache_service = CacheService()


@router.get("/stats")
def get_cache_stats() -> Dict[str, Any]:
    """Get Redis cache statistics"""
    stats = cache_service.get_cache_stats()
    return {
        "cache_stats": stats,
        "message": "Cache statistics retrieved successfully"
    }


@router.delete("/clear")
def clear_cache() -> Dict[str, str]:
    """Clear all cached data"""
    success = cache_service.clear_cache()
    if success:
        return {"message": "Cache cleared successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to clear cache")
