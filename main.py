# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI()

# existing health check
@app.get("/ping", response_class=PlainTextResponse)
def ping() -> str:
    return "pong"

# in memory sample data
recipes = [
    {
        "id": 1,
        "title": "Garlic Shrimp Pasta",
        "ingredients": ["shrimp", "pasta", "garlic", "olive oil", "lemon"],
        "steps": ["boil pasta", "saute garlic and shrimp", "toss together"],
    },
    {
        "id": 2,
        "title": "Chicken Rice Bowl",
        "ingredients": ["chicken", "rice", "soy sauce", "green onion"],
        "steps": ["cook rice", "pan sear chicken", "slice and serve"],
    },
    {
        "id": 3,
        "title": "Simple Salad",
        "ingredients": ["lettuce", "tomato", "cucumber", "olive oil"],
        "steps": ["chop veggies", "dress and toss"],
    },
]

@app.get("/recipes")
def list_recipes():
    return recipes

@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int):
    for r in recipes:
        if r["id"] == recipe_id:
            return r
    raise HTTPException(status_code=404, detail="Recipe not found")
