from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.database import SessionLocal
from typing import Optional


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session, token: str) -> Optional[User]:
    # Token orqali foydalanuvchini olish logikasi
    # Misol uchun, tokenni dekodlash va foydalanuvchi ma'lumotlarini olish
    pass


def is_nazoratchi(token: str, db: Session = Depends(get_db)) -> User:
    current_user = get_current_user(db, token)
    if not current_user or current_user.role != "NAZORATCHI":
        raise HTTPException(status_code=403, detail="Access forbidden")
    return current_user
