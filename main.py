from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from typing import List, Dict, Any

app = FastAPI()

@app.get("/ping", response_class=PlainTextResponse)
def ping() -> str:
    return "pong"

# In-memory storage with full recipe fields
recipes: List[Dict[str, Any]] = [
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

next_id = 4  # Tracks the next available recipe ID

# READ - all
@app.get("/recipes")
def list_recipes():
    return recipes

# READ - single
@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int):
    for r in recipes:
        if r["id"] == recipe_id:
            return r
    raise HTTPException(status_code=404, detail="Recipe not found")

# CREATE
@app.post("/recipes", status_code=201)
def create_recipe(recipe: Dict[str, Any]):
    global next_id
    recipe["id"] = next_id
    next_id += 1
    recipes.append(recipe)
    return recipe

# UPDATE
@app.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, updated_recipe: Dict[str, Any]):
    for idx, r in enumerate(recipes):
        if r["id"] == recipe_id:
            updated_recipe["id"] = recipe_id  # keep same ID
            recipes[idx] = updated_recipe
            return updated_recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

# DELETE
@app.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int):
    for idx, r in enumerate(recipes):
        if r["id"] == recipe_id:
            recipes.pop(idx)
            return
    raise HTTPException(status_code=404, detail="Recipe not found")
