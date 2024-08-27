from datetime import datetime

from sqlalchemy.orm import relationship


from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Boolean
import enum
from app.database import Base


class RoleEnum(str, enum.Enum):
    NAZORATCHI = "NAZORATCHI"
    AFISSANT = "AFISSANT"
    HODIM = "HODIM"
    USER = "USER"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), nullable=False)

    orders = relationship('Order', back_populates='user')
    reservations = relationship('Reservation', back_populates='user')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    menu_id = Column(Integer, ForeignKey('menus.id'))
    quantity = Column(Integer)
    status = Column(String)  # 'pending', 'accepted', 'completed'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    menu = relationship("Menu", back_populates="orders")


class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    table_number = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="reservations")


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String)

    orders = relationship('Order', back_populates='menu')

