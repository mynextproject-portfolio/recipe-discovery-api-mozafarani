import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.core.app import create_app
from app.repositories.recipe_repository import InMemoryRecipeRepository
from app.services.recipe_service import RecipeService
from app.dependencies import get_recipe_service


# Create a shared test repository that persists across requests
test_repository = InMemoryRecipeRepository()
test_service = RecipeService(test_repository)


def get_test_recipe_service():
    """Test dependency that returns the shared test service"""
    return test_service


# Create test app with dependency override
app = create_app()
app.dependency_overrides[get_recipe_service] = get_test_recipe_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_test_data():
    """Reset test data before each test"""
    # Clear the test repository and reinitialize with default data
    test_repository.recipes.clear()
    test_repository.recipes.extend([
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
    ])
    test_repository.next_id = 4


def test_ping():
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.text == "pong"


def test_list_recipes_initial():
    resp = client.get("/recipes")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "title" in data[0]


def test_get_existing_recipe():
    resp = client.get("/recipes/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert "title" in data


def test_get_non_existing_recipe():
    resp = client.get("/recipes/99999")
    assert resp.status_code == 404


def test_search_recipes_case_insensitive():
    resp_lower = client.get("/recipes/search?q=pasta")
    resp_upper = client.get("/recipes/search?q=PASTA")
    assert resp_lower.status_code == 200
    assert resp_upper.status_code == 200
    assert resp_lower.json() == resp_upper.json()
    # ensure at least one match for "pasta"
    assert any("pasta" in r["title"].lower() for r in resp_lower.json())


def test_search_recipes_empty_query():
    resp = client.get("/recipes/search?q=")
    assert resp.status_code == 200
    assert resp.json() == []


def test_search_recipes_no_match():
    resp = client.get("/recipes/search?q=nonexistentfood")
    assert resp.status_code == 200
    assert resp.json() == []


def test_happy_path_crud_and_search():
    # Create
    new_recipe = {
        "title": "Test Dish",
        "ingredients": ["ingredient1", "ingredient2"],
        "steps": ["Step 1", "Step 2"],
        "prepTime": "5 minutes",
        "cookTime": "10 minutes",
        "difficulty": "Medium",
        "cuisine": "TestCuisine"
    }
    resp_create = client.post("/recipes", json=new_recipe)
    assert resp_create.status_code == 201
    created = resp_create.json()
    assert "id" in created
    recipe_id = created["id"]

    # Get created
    resp_get = client.get(f"/recipes/{recipe_id}")
    assert resp_get.status_code == 200
    fetched = resp_get.json()
    assert fetched["title"] == "Test Dish"

    # Search for created
    resp_search = client.get(f"/recipes/search?q=Test")
    assert resp_search.status_code == 200
    search_results = resp_search.json()
    assert any(r["id"] == recipe_id for r in search_results)

    # Update
    updated_recipe = {
        "title": "Updated Test Dish",
        "ingredients": ["ingredient1", "ingredient2", "ingredient3"],
        "steps": ["Updated step 1", "Updated step 2"],
        "prepTime": "6 minutes",
        "cookTime": "12 minutes",
        "difficulty": "Easy",
        "cuisine": "UpdatedCuisine"
    }
    resp_update = client.put(f"/recipes/{recipe_id}", json=updated_recipe)
    assert resp_update.status_code == 200
    updated = resp_update.json()
    assert updated["title"] == "Updated Test Dish"
    assert "ingredient3" in updated["ingredients"]

    # Verify update
    resp_get_updated = client.get(f"/recipes/{recipe_id}")
    assert resp_get_updated.status_code == 200
    assert resp_get_updated.json()["title"] == "Updated Test Dish"

    # Delete
    resp_delete = client.delete(f"/recipes/{recipe_id}")
    assert resp_delete.status_code == 204

    # Verify deletion
    resp_get_deleted = client.get(f"/recipes/{recipe_id}")
    assert resp_get_deleted.status_code == 404
