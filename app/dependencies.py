from fastapi import Depends
from app.repositories.recipe_repository import RecipeRepository, InMemoryRecipeRepository
from app.services.recipe_service import RecipeService


def get_recipe_repository() -> RecipeRepository:
    """Dependency to get recipe repository instance"""
    return InMemoryRecipeRepository()


def get_recipe_service(repository: RecipeRepository = Depends(get_recipe_repository)) -> RecipeService:
    """Dependency to get recipe service instance"""
    return RecipeService(repository)
