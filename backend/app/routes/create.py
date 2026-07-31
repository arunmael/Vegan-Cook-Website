from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.app.db import get_db


app = FastAPI(title="Vegan Cook Website")

@app.post("/api/create-user")
def create_user(user_name: str, user_email: str, user_password: str, db: Session = Depends(get_db)):