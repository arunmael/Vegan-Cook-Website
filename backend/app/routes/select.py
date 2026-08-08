import hashlib
import secrets


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.model import User
from backend.app.schema import Login, UserCreate, UserMailCheck, UserNameCheck, UserResponse, UserLoginEmail, UserLoginName


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
            detail="Invalid password or E-Mail/ Username.",
        )

    # Überprüfen Sie das Passwort
    if not verify_password(user_data.user_password, user.user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password or E-Mail/ Username.",
        )
    current_user = user.user_id
    

    return {"message": "Login successful", "user": current_user}



@router.post("/api/login-user-name")
def login_user_name(user_data: UserLoginName, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == user_data.user_name).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid password or E-Mail/ Username.",
        )

    # Überprüfen Sie das Passwort
    if not verify_password(user_data.user_password, user.user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password or E-Mail/ Username.",
        )
    current_user = user.user_id
    

    return {"message": "Login successful", "user": current_user}



@router.post("/api/select-user-mail")
def select_user_mail(user_data: UserMailCheck, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_email == user_data.user_email).first()
    if not user:
        is_email = False
        return is_email

    is_email = True
    return is_email


@router.post("/api/select-user-name")
def select_user_name(user_data: UserNameCheck, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == user_data.user_name).first()
    if not user:
        is_name = False
        return is_name

    is_name = True
    return is_name



@router.post("/api/login")
def login_user(user_data: Login, db: Session = Depends(get_db)):
    mail_check = UserMailCheck(user_email=user_data.identifier)
    result = select_user_mail(mail_check, db)
    if result is True:
        email_login = UserLoginEmail(user_email=user_data.identifier, user_password=user_data.user_password)
        user_id = login_user_email(email_login, db)
        return user_id
    
    name_check = UserNameCheck(user_name=user_data.identifier)
    result = select_user_name(name_check, db)
    if result is True:
        name_login = UserLoginName(user_name=user_data.identifier, user_password=user_data.user_password)
        user_id = login_user_name(name_login, db)
        return user_id
    
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid password or E-Mail/ Username.",
        )
