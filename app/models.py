import enum
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship


Base = declarative_base()
# Toshkent vaqt zonasini o'rnatish

class RoleEnum(str, enum.Enum):
    NAZORATCHI = "NAZORATCHI"
    AFISSANT = "AFISSANT"
    HODIM = "HODIM"
    USER = "USER"


class TableStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    hashed_password = Column(String)
    role = Column(SqlEnum(RoleEnum), index=True)  # Enum uchun SqlEnum

    orders = relationship('Order', back_populates='user')
    reservations = relationship('Reservation', back_populates='user')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    menu_id = Column(Integer, ForeignKey('menus.id'))
    table_id = Column(Integer, ForeignKey('tables.id'))
    quantity = Column(Integer)
    status = Column(String)
    delivery_time = Column(DateTime, nullable=True)  # Ensure this line is present
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='orders')
    menu = relationship('Menu', back_populates='orders')
    table = relationship('Table', back_populates='orders')


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String)

    orders = relationship("Order", back_populates="menu")  # `Order` modelida `menu` xususiyati bilan bog'langan


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    table_id = Column(Integer, ForeignKey("tables.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    table = relationship("Table", back_populates="reservations")

    user = relationship("User", back_populates="reservations")
    table = relationship("Table", back_populates="reservations")

    def update_table_status(self, db):
        if self.end_time < datetime.utcnow():
            self.table.status = TableStatus.AVAILABLE
        else:
            self.table.status = TableStatus.RESERVED

        db.add(self.table)
        db.commit()


class Table(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer, unique=True, index=True)
    description = Column(String, nullable=True)
    capacity = Column(Integer)
    status = Column(SqlEnum(TableStatus), default=TableStatus.AVAILABLE)

    reservations = relationship("Reservation", back_populates="table")
    orders = relationship("Order", back_populates="table")