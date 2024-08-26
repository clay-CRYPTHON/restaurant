# Import necessary modules
from typing import List
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models, schemas, database
from app.models import User
from app.settings import Settings
from app.schemas import UserLogin
import datetime


@AuthJWT.load_config
def get_config():
    return Settings()


users_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# Function to get user by username or email
def get_user_by_username_or_email(db: Session, identifier: str):
    return db.query(User).filter((User.email == identifier) | (User.username == identifier)).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


@users_router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Yangi foydalanuvchini yaratish va bazaga qo'shish
    new_user = models.User(
        username=user.username,
        email=user.email,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Bu qator yangi foydalanuvchidan ID va boshqa ma'lumotlarni oladi

    return new_user  # Bu qatorni ma'lumotni qaytarish uchun yangilang


@users_router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
async def get_users(db: Session = Depends(database.get_db), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Enter valid access token")

    users = db.query(User).all()
    return users


@users_router.post("/login")
def login(user: UserLogin, db: Session = Depends(database.get_db), Authorize: AuthJWT = Depends()):
    db_user = get_user_by_username_or_email(db, user.username_or_email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username/email or password")

    access_token = Authorize.create_access_token(subject=db_user.email)
    refresh_token = Authorize.create_refresh_token(subject=db_user.email)

    token = {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }

    response = {
        'success': True,
        'code': 200,
        'message': 'You are now logged in',
        'token': token
    }

    return jsonable_encoder(response)


@users_router.post("/logout")
def logout(Authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)):
    Authorize.jwt_required()

    user_email = Authorize.get_jwt_subject()

    # Foydalanuvchi topish
    user = db.query(models.User).filter(models.User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # Foydalanuvchining JWT tokenini bekor qilish
    user.current_jwt_token = None
    db.commit()

    return {"message": "Successfully logged out"}


# Refresh token function
@users_router.post("/login/refresh")
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        access_lifetime = datetime.timedelta(minutes=60)
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        db_user = Session.query(User).filter(User.username == current_user).first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        new_access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        response_model = {
            'success': True,
            'code': 200,
            'message': 'New access token is created',
            'data': {
                'access_token': new_access_token,
            }
        }
        return response_model

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Refresh token")


# Function to get current user
@users_router.get("/me", response_model=schemas.UserResponse)
def get_user(Authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)):
    Authorize.jwt_required()

    current_user_email = Authorize.get_jwt_subject()
    db_user = get_user_by_email(db, current_user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Function to update current user
@users_router.put("/me", response_model=schemas.UserResponse)
def update_user(user: schemas.UserBase, Authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)):
    Authorize.jwt_required()

    current_user_email = Authorize.get_jwt_subject()
    db_user = get_user_by_email(db, current_user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.username = user.username
    db_user.email = user.email
    db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user
