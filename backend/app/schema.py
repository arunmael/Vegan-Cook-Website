from pydantic import BaseModel, ConfigDict, Field


class IngredientCreate(BaseModel):
    """Daten, die beim Erstellen einer Zutat erwartet werden."""

    ing_name: str = Field(min_length=1, max_length=255)


class IngredientResponse(BaseModel):
    """Daten, die FastAPI für eine Zutat zurückgibt."""

    ingredient_id: int
    ing_name: str

    model_config = ConfigDict(from_attributes=True)
