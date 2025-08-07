from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.models.recipe import RecipeCreate, RecipeUpdate
from app.services.recipe_service import recipe_service

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("")
def list_recipes() -> List[Dict[str, Any]]:
    """Get all recipes"""
    return recipe_service.get_all_recipes()


@router.get("/search")
def search_recipes(q: str = "") -> List[Dict[str, Any]]:
    """Search recipes by title (case-insensitive)"""
    return recipe_service.search_recipes(q)


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int) -> Dict[str, Any]:
    """Get a recipe by ID"""
    recipe = recipe_service.get_recipe_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("", status_code=201)
def create_recipe(recipe: RecipeCreate) -> Dict[str, Any]:
    """Create a new recipe"""
    return recipe_service.create_recipe(recipe)


@router.put("/{recipe_id}")
def update_recipe(recipe_id: int, updated_recipe: RecipeUpdate) -> Dict[str, Any]:
    """Update an existing recipe"""
    recipe = recipe_service.update_recipe(recipe_id, updated_recipe)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int) -> None:
    """Delete a recipe by ID"""
    if not recipe_service.delete_recipe(recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")
