from typing import List, Dict, Any, Optional
from app.models.recipe import RecipeCreate, RecipeUpdate
from app.repositories.recipe_repository import RecipeRepository
from app.services.mealdb_service import MealDBService


class RecipeService:
    def __init__(self, repository: RecipeRepository):
        self.repository = repository
        self.mealdb_service = MealDBService()

    def get_all_recipes(self) -> List[Dict[str, Any]]:
        """Get all recipes"""
        return self.repository.get_all_recipes()

    def get_recipe_by_id(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """Get a recipe by ID"""
        return self.repository.get_recipe_by_id(recipe_id)

    def search_recipes(self, query: str) -> List[Dict[str, Any]]:
        """Search recipes by title (case-insensitive) - combines internal and MealDB results"""
        # Get internal recipes
        internal_recipes = self.repository.search_recipes(query)
        
        # Add source field to internal recipes
        for recipe in internal_recipes:
            recipe["source"] = "internal"
        
        # Get MealDB recipes
        mealdb_recipes = self.mealdb_service.search_recipes(query)
        
        # Combine results (internal first, then MealDB)
        combined_results = internal_recipes + mealdb_recipes
        
        return combined_results

    def create_recipe(self, recipe_data: RecipeCreate) -> Dict[str, Any]:
        """Create a new recipe"""
        return self.repository.create_recipe(recipe_data)

    def update_recipe(self, recipe_id: int, recipe_data: RecipeUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing recipe"""
        return self.repository.update_recipe(recipe_id, recipe_data)

    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete a recipe by ID"""
        return self.repository.delete_recipe(recipe_id)
