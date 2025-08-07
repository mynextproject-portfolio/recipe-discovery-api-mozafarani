# Recipe Discovery API

A FastAPI-based recipe management API with full CRUD operations and search functionality.

## Project Structure

The application follows a well-organized structure that separates different concerns:

```
recipe-discovery-api-mozafarani/
├── app/
│   ├── __init__.py
│   ├── api/                    # API routes using FastAPI APIRouter
│   │   ├── __init__.py
│   │   ├── health.py          # Health check endpoints
│   │   └── recipes.py         # Recipe CRUD endpoints
│   ├── core/                  # Core application components
│   │   ├── __init__.py
│   │   └── app.py            # FastAPI app factory
│   ├── models/               # Pydantic data models
│   │   ├── __init__.py
│   │   └── recipe.py         # Recipe data models
│   └── services/             # Business logic layer
│       ├── __init__.py
│       └── recipe_service.py # Recipe business logic
├── main.py                   # Application entry point
├── test_ping.py             # Health check tests
├── test_integration.py      # Integration tests
└── README.md
```

## Features

- **Health Check**: `/ping` endpoint for monitoring
- **Recipe Management**: Full CRUD operations for recipes
- **Search**: Case-insensitive search by recipe title
- **In-Memory Storage**: Simple in-memory data storage
- **Pydantic Models**: Type-safe data validation
- **FastAPI Best Practices**: Proper router organization and dependency injection

## API Endpoints

### Health Check
- `GET /ping` - Health check endpoint

### Recipes
- `GET /recipes` - List all recipes
- `GET /recipes/search?q={query}` - Search recipes by title
- `GET /recipes/{recipe_id}` - Get a specific recipe
- `POST /recipes` - Create a new recipe
- `PUT /recipes/{recipe_id}` - Update an existing recipe
- `DELETE /recipes/{recipe_id}` - Delete a recipe

## Running the Application

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn pytest
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Run tests:
   ```bash
   python3 -m pytest test_ping.py test_integration.py -v
   ```

## Development

The application follows FastAPI and Python best practices:

- **Separation of Concerns**: Routes, models, and business logic are separated
- **APIRouter**: Routes are organized using FastAPI's APIRouter
- **Type Safety**: Pydantic models ensure data validation
- **Clean Architecture**: Business logic is separated from API layer
- **Testable**: All functionality is covered by tests

## Data Models

The application uses Pydantic models for type safety:

- `Recipe`: Complete recipe model with optional ID
- `RecipeCreate`: Model for creating new recipes
- `RecipeUpdate`: Model for updating existing recipes

All models include fields for title, ingredients, steps, prep time, cook time, difficulty, and cuisine.
