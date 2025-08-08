import sqlite3
import json
from typing import List, Dict, Any, Optional
from app.models.recipe import RecipeCreate, RecipeUpdate
from app.repositories.recipe_repository import RecipeRepository


class SQLiteRecipeRepository(RecipeRepository):
    """SQLite implementation of recipe repository"""
    
    def __init__(self, db_path: str = "recipes.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with the recipes table"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    ingredients TEXT NOT NULL,
                    steps TEXT NOT NULL,
                    prepTime TEXT NOT NULL,
                    cookTime TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    cuisine TEXT NOT NULL
                )
            ''')
            conn.commit()
            
            # Check if we need to seed initial data
            cursor.execute("SELECT COUNT(*) FROM recipes")
            if cursor.fetchone()[0] == 0:
                self._seed_initial_data()
    
    def _seed_initial_data(self):
        """Seed the database with initial recipe data"""
        initial_recipes = [
            {
                "title": "Garlic Shrimp Pasta",
                "ingredients": ["shrimp", "pasta", "garlic", "olive oil", "lemon"],
                "steps": ["Boil pasta", "Saute garlic and shrimp", "Toss together"],
                "prepTime": "10 minutes",
                "cookTime": "15 minutes",
                "difficulty": "Easy",
                "cuisine": "Italian"
            },
            {
                "title": "Chicken Rice Bowl",
                "ingredients": ["chicken", "rice", "soy sauce", "green onion"],
                "steps": ["Cook rice", "Pan sear chicken", "Slice and serve"],
                "prepTime": "15 minutes",
                "cookTime": "20 minutes",
                "difficulty": "Easy",
                "cuisine": "Asian"
            },
            {
                "title": "Simple Salad",
                "ingredients": ["lettuce", "tomato", "cucumber", "olive oil"],
                "steps": ["Chop veggies", "Dress and toss"],
                "prepTime": "5 minutes",
                "cookTime": "0 minutes",
                "difficulty": "Easy",
                "cuisine": "Mediterranean"
            },
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for recipe in initial_recipes:
                cursor.execute('''
                    INSERT INTO recipes (title, ingredients, steps, prepTime, cookTime, difficulty, cuisine)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    recipe["title"],
                    json.dumps(recipe["ingredients"]),
                    json.dumps(recipe["steps"]),
                    recipe["prepTime"],
                    recipe["cookTime"],
                    recipe["difficulty"],
                    recipe["cuisine"]
                ))
            conn.commit()
    
    def _dict_from_row(self, row: tuple) -> Dict[str, Any]:
        """Convert a database row to a dictionary"""
        return {
            "id": row[0],
            "title": row[1],
            "ingredients": json.loads(row[2]),
            "steps": json.loads(row[3]),
            "prepTime": row[4],
            "cookTime": row[5],
            "difficulty": row[6],
            "cuisine": row[7]
        }
    
    def get_all_recipes(self) -> List[Dict[str, Any]]:
        """Get all recipes"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes ORDER BY id")
            rows = cursor.fetchall()
            return [self._dict_from_row(row) for row in rows]
    
    def get_recipe_by_id(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """Get a recipe by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
            row = cursor.fetchone()
            return self._dict_from_row(row) if row else None
    
    def search_recipes(self, query: str) -> List[Dict[str, Any]]:
        """Search recipes by title (case-insensitive)"""
        if not query.strip():
            return []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM recipes WHERE LOWER(title) LIKE LOWER(?) ORDER BY id",
                (f"%{query}%",)
            )
            rows = cursor.fetchall()
            return [self._dict_from_row(row) for row in rows]
    
    def create_recipe(self, recipe_data: RecipeCreate) -> Dict[str, Any]:
        """Create a new recipe"""
        recipe_dict = recipe_data.model_dump()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recipes (title, ingredients, steps, prepTime, cookTime, difficulty, cuisine)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                recipe_dict["title"],
                json.dumps(recipe_dict["ingredients"]),
                json.dumps(recipe_dict["steps"]),
                recipe_dict["prepTime"],
                recipe_dict["cookTime"],
                recipe_dict["difficulty"],
                recipe_dict["cuisine"]
            ))
            recipe_id = cursor.lastrowid
            conn.commit()
            
            # Return the created recipe with the generated ID
            recipe_dict["id"] = recipe_id
            return recipe_dict
    
    def update_recipe(self, recipe_id: int, recipe_data: RecipeUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing recipe"""
        recipe_dict = recipe_data.model_dump()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE recipes 
                SET title = ?, ingredients = ?, steps = ?, prepTime = ?, cookTime = ?, difficulty = ?, cuisine = ?
                WHERE id = ?
            ''', (
                recipe_dict["title"],
                json.dumps(recipe_dict["ingredients"]),
                json.dumps(recipe_dict["steps"]),
                recipe_dict["prepTime"],
                recipe_dict["cookTime"],
                recipe_dict["difficulty"],
                recipe_dict["cuisine"],
                recipe_id
            ))
            
            if cursor.rowcount == 0:
                return None
            
            conn.commit()
            
            # Return the updated recipe
            recipe_dict["id"] = recipe_id
            return recipe_dict
    
    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete a recipe by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            conn.commit()
            return cursor.rowcount > 0
