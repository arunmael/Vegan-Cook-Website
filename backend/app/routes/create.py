import hashlib
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.model import User, Ingredient
from backend.app.schema import UserCreate, UserResponse, IngredientCreate

router = APIRouter()


def hash_password(password: str) -> str:
    """Erstellt aus einem Passwort einen gesalzenen PBKDF2-Hash."""
    iterations = 600_000
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        iterations,
    ).hex()

    return f"pbkdf2_sha256${iterations}${salt}${password_hash}"


@router.post(
    "/api/create-user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        user_name=user_data.user_name,
        user_email=user_data.user_email,
        user_password=hash_password(user_data.user_password),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Benutzername oder E-Mail ist bereits vergeben.",
        )

    return new_user



@router.post("/api/create-ingredient")
def create_ingredient(
    ingredient_data: IngredientCreate,
    db: Session = Depends(get_db),
):
    ingredient_name = ingredient_data.ing_name.strip()
    if not ingredient_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The Ingredient name cannot be empty.",
        )

    existing_ingredient = (
        db.query(Ingredient)
        .filter(Ingredient.ing_name.ilike(ingredient_name))
        .first()
    )
    if existing_ingredient is not None:
        ingredient_id = existing_ingredient.ingredient_id
        return ingredient_id

    new_ingredient = Ingredient(ing_name=ingredient_name)

    try:
        db.add(new_ingredient)
        db.commit()
        db.refresh(new_ingredient)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The Ingredient could not be created.",
        )

    ingredient_id = new_ingredient.ingredient_id
    return ingredient_id
