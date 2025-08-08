import requests
import re
from typing import List, Dict, Any, Optional


class MealDBService:
    """Service for interacting with TheMealDB API"""
    
    def __init__(self, base_url: str = "https://www.themealdb.com/api/json/v1/1"):
        self.base_url = base_url
    
    def search_recipes(self, query: str) -> List[Dict[str, Any]]:
        """Search recipes in MealDB by name"""
        if not query.strip():
            return []
        
        try:
            response = requests.get(f"{self.base_url}/search.php", params={"s": query})
            response.raise_for_status()
            data = response.json()
            
            if not data.get("meals"):
                return []
            
            return [self._transform_mealdb_recipe(meal) for meal in data["meals"]]
        
        except (requests.RequestException, KeyError, ValueError) as e:
            # Log error in production, but return empty list for now
            print(f"Error fetching from MealDB: {e}")
            return []
    
    def _transform_mealdb_recipe(self, meal: Dict[str, Any]) -> Dict[str, Any]:
        """Transform MealDB recipe format to our internal format"""
        # Extract ingredients (MealDB has strIngredient1-20 fields)
        ingredients = []
        for i in range(1, 21):
            ingredient_key = f"strIngredient{i}"
            measure_key = f"strMeasure{i}"
            
            ingredient = meal.get(ingredient_key)
            measure = meal.get(measure_key)
            
            # Handle None values and empty strings
            if ingredient and ingredient != "null" and ingredient.strip():
                ingredient = ingredient.strip()
                measure = measure.strip() if measure else ""
                
                if measure:
                    ingredients.append(f"{measure} {ingredient}")
                else:
                    ingredients.append(ingredient)
        
        # Extract steps from instructions
        instructions = meal.get("strInstructions", "")
        steps = self._parse_instructions_to_steps(instructions)
        
        # Determine difficulty based on ingredients count and steps
        difficulty = self._determine_difficulty(len(ingredients), len(steps))
        
        # Estimate prep and cook time (MealDB doesn't provide this)
        prep_time = "15 minutes"  # Default estimate
        cook_time = "30 minutes"  # Default estimate
        
        return {
            "id": meal.get("idMeal", ""),
            "title": meal.get("strMeal", ""),
            "ingredients": ingredients,
            "steps": steps,
            "prepTime": prep_time,
            "cookTime": cook_time,
            "difficulty": difficulty,
            "cuisine": meal.get("strArea", "Unknown"),
            "source": "mealdb"
        }
    
    def _parse_instructions_to_steps(self, instructions: str) -> List[str]:
        """Parse MealDB instructions into step-by-step format"""
        if not instructions:
            return []
        
        # Clean up the instructions
        instructions = instructions.replace('\r\n', '\n').replace('\r', '\n')
        
        # Split by common step indicators
        step_patterns = [
            r'STEP\s+\d+[:\s]*',  # STEP 1:, STEP 2:, etc.
            r'\d+\.\s*',           # 1., 2., etc.
            r'^\s*[A-Z][^.]*\.',   # Sentences starting with capital letters
        ]
        
        # Try to find steps using patterns
        for pattern in step_patterns:
            steps = re.split(pattern, instructions, flags=re.IGNORECASE | re.MULTILINE)
            if len(steps) > 1:
                # Clean up steps
                cleaned_steps = []
                for step in steps[1:]:  # Skip the first empty part
                    step = step.strip()
                    if step and len(step) > 10:  # Only include substantial steps
                        cleaned_steps.append(step)
                
                if cleaned_steps:
                    return cleaned_steps
        
        # If no clear steps found, split by sentences
        sentences = re.split(r'[.!?]+', instructions)
        steps = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        
        return steps[:10]  # Limit to 10 steps
    
    def _determine_difficulty(self, ingredient_count: int, step_count: int) -> str:
        """Determine recipe difficulty based on ingredients and steps"""
        total_complexity = ingredient_count + step_count
        
        if total_complexity <= 8:
            return "Easy"
        elif total_complexity <= 15:
            return "Medium"
        else:
            return "Hard"
