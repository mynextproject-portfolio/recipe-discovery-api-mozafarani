import os
from fastapi import Depends
from app.repositories.recipe_repository import RecipeRepository, InMemoryRecipeRepository
from app.repositories.sqlite_recipe_repository import SQLiteRecipeRepository
from app.services.recipe_service import RecipeService
from app.services.mealdb_service import MealDBService


def get_recipe_repository() -> RecipeRepository:
    """Dependency to get recipe repository instance"""
    return SQLiteRecipeRepository()


def get_mealdb_service() -> MealDBService:
    """Dependency to get MealDB service instance with Redis caching"""
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    return MealDBService(redis_url=redis_url)


def get_recipe_service(
    repository: RecipeRepository = Depends(get_recipe_repository),
    mealdb_service: MealDBService = Depends(get_mealdb_service)
) -> RecipeService:
    """Dependency to get recipe service instance"""
    return RecipeService(repository, mealdb_service)
