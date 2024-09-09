from fastapi import HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
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


def get_current_user(Authorize: AuthJWT = Depends()):
    pass


def is_nazoratchi(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        raw_jwt = Authorize.get_raw_jwt()
        user_role = raw_jwt.get("role")

        if user_role != "NAZORATCHI":
            raise HTTPException(status_code=403, detail="Access forbidden: Insufficient permissions")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
