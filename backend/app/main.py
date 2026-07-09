from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from backend.app.db import engine


BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="Vegan Cook Website")


@app.get("/api/health")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "reachable",
    }


@app.get("/api/recipes")
def list_recipes():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT id, title, description, created_at
                FROM recipes
                ORDER BY created_at DESC
            """)
        )

        recipes = [
            {
                "id": row.id,
                "title": row.title,
                "description": row.description,
                "created_at": row.created_at.isoformat(),
            }
            for row in result
        ]

    return {"recipes": recipes}


app.mount(
    "/",
    StaticFiles(directory=str(FRONTEND_DIR), html=True),
    name="frontend",
)

