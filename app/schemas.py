import pytz
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class UserBase(BaseModel):
    username: str
    phone_number: str
    role: str  # 'nazoratchi', 'afissant', 'user', 'hodim' bo'lishi mumkin


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    phone_number: str
    role: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    phone_number: str
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

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class OrderCreate(BaseModel):
    menu_id: int
    quantity: int
    table_id: int
    status: OrderStatus

    class Config:
        orm_mode = True


class OrderUpdate(BaseModel):
    status: OrderStatus

    class Config:
        orm_mode = True


class OrderResponse(BaseModel):
    id: int
    table_id: int
    menu_id: int
    quantity: int
    status: str

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: int
    user_id: int
    table_id: int
    menu_id: int
    quantity: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    delivery_time: Optional[datetime] = None

    class Config:
        orm_mode = True


class OrderHistory(BaseModel):
    orders: list[Order]

    class Config:
        orm_mode = True


class MenuItem(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True


class Table(BaseModel):
    id: int
    number: int
    status: str  # RESERVED yoki AVAILABLE

    class Config:
        orm_mode = True




class ReservationCreate(BaseModel):
    user_id: int
    table_id: int  # table_number o'rniga table_id
    start_time: datetime
    end_time: datetime
    is_active: bool = True

    class Config:
        orm_mode = True

    def local_create_time(self):
        timezone = pytz.timezone('Asia/Tashkent')
        return self.create.astimezone(timezone)



class ReservationUpdate(BaseModel):
    table_number: int
    start_time: datetime
    end_time: datetime
    is_active: bool


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    table_id: int
    start_time: datetime
    end_time: datetime
    is_active: bool

    class Config:
        orm_mode = True



class TableStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"

class TableBase(BaseModel):
    table_number: int
    capacity: int
    status: TableStatus = TableStatus.AVAILABLE

class TableCreate(TableBase):
    pass

class TableUpdate(BaseModel):
    capacity: Optional[int] = None
    status: Optional[TableStatus] = None


class TableInDB(TableBase):
    id: int

    class Config:
        orm_mode = True



932470980
936275060