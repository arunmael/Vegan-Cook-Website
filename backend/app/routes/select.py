import hashlib
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.model import User
from backend.app.schema import UserCreate, UserResponse, UserLoginEmail, UserLoginName


router = APIRouter()


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt, expected_hash = stored_hash.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            int(iterations),
        ).hex()

        return secrets.compare_digest(calculated_hash, expected_hash)
    except (ValueError, TypeError):
        return False


@router.post("/api/login-user-email")
def login_user_email(user_data: UserLoginEmail, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_email == user_data.user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid password or E-Mail.",
        )

    # Überprüfen Sie das Passwort
    if not verify_password(user_data.user_password, user.user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password or E-Mail.",
        )

    return {"message": "Login successful", "user_id": user.user_id}