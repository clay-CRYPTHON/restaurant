from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str  # 'nazoratchi', 'afissant', 'user', 'hodim' bo'lishi mumkin


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True


class MenuBase(BaseModel):
    name: str
    price: float
    description: Optional[str]


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class Menu(MenuBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    user_id: int
    menu_id: int
    quantity: int
    status: Optional[str] = "pending"  # Default status: 'pending'


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ReservationBase(BaseModel):
    user_id: int
    table_number: int
    start_time: datetime
    end_time: datetime
    is_active: Optional[bool] = True


class ReservationCreate(ReservationBase):
    pass


class ReservationResponse(ReservationBase):
    id: int

    class Config:
        orm_mode = True
