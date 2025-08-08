from fastapi import FastAPI
from app.api import health, recipes, cache


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Recipe Discovery API",
        description="A simple recipe management API with Redis caching",
        version="1.0.0"
    )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(recipes.router)
    app.include_router(cache.router)
    
    return app


# Create the app instance
app = create_app()
