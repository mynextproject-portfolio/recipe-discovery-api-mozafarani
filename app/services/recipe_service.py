from typing import List, Dict, Any, Optional
from app.models.recipe import Recipe, RecipeCreate, RecipeUpdate


class RecipeService:
    def __init__(self):
        # In-memory storage with full recipe fields
        self.recipes: List[Dict[str, Any]] = [
            {
                "id": 1,
                "title": "Garlic Shrimp Pasta",
                "ingredients": ["shrimp", "pasta", "garlic", "olive oil", "lemon"],
                "steps": ["Boil pasta", "Saute garlic and shrimp", "Toss together"],
                "prepTime": "10 minutes",
                "cookTime": "15 minutes",
                "difficulty": "Easy",
                "cuisine": "Italian"
            },
            {
                "id": 2,
                "title": "Chicken Rice Bowl",
                "ingredients": ["chicken", "rice", "soy sauce", "green onion"],
                "steps": ["Cook rice", "Pan sear chicken", "Slice and serve"],
                "prepTime": "15 minutes",
                "cookTime": "20 minutes",
                "difficulty": "Easy",
                "cuisine": "Asian"
            },
            {
                "id": 3,
                "title": "Simple Salad",
                "ingredients": ["lettuce", "tomato", "cucumber", "olive oil"],
                "steps": ["Chop veggies", "Dress and toss"],
                "prepTime": "5 minutes",
                "cookTime": "0 minutes",
                "difficulty": "Easy",
                "cuisine": "Mediterranean"
            },
        ]
        self.next_id = 4  # Tracks the next available recipe ID

    def get_all_recipes(self) -> List[Dict[str, Any]]:
        """Get all recipes"""
        return self.recipes

    def get_recipe_by_id(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """Get a recipe by ID"""
        for recipe in self.recipes:
            if recipe["id"] == recipe_id:
                return recipe
        return None

    def search_recipes(self, query: str) -> List[Dict[str, Any]]:
        """Search recipes by title (case-insensitive)"""
        if not query.strip():
            return []
        
        query_lower = query.lower()
        return [recipe for recipe in self.recipes if query_lower in recipe["title"].lower()]

    def create_recipe(self, recipe_data: RecipeCreate) -> Dict[str, Any]:
        """Create a new recipe"""
        recipe_dict = recipe_data.model_dump()
        recipe_dict["id"] = self.next_id
        self.next_id += 1
        self.recipes.append(recipe_dict)
        return recipe_dict

    def update_recipe(self, recipe_id: int, recipe_data: RecipeUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing recipe"""
        for idx, recipe in enumerate(self.recipes):
            if recipe["id"] == recipe_id:
                updated_recipe = recipe_data.model_dump()
                updated_recipe["id"] = recipe_id  # keep same ID
                self.recipes[idx] = updated_recipe
                return updated_recipe
        return None

    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete a recipe by ID"""
        for idx, recipe in enumerate(self.recipes):
            if recipe["id"] == recipe_id:
                self.recipes.pop(idx)
                return True
        return False


# Global instance
recipe_service = RecipeService()
