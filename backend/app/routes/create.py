import hashlib
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.model import User
from backend.app.schema import UserCreate, UserResponse


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
