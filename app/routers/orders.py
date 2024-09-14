from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.models import Order, Menu, Table
from app.routers.auth import get_current_user  # Bu sizning JWT autentifikatsiyangiz bo'lsa
from app.permission import is_nazoratchi# Rollar bo'yicha tekshirish uchun
from app.schemas import OrderCreate

order_router = APIRouter()


@order_router.post("/make", response_model=OrderCreate)
def make_order(order: OrderCreate, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()

    # Menu va stolni tekshirish
    menu = db.query(Menu).filter(Menu.id == order.menu_id).first()  # To'g'ri tekshirish
    table = db.query(Table).filter(Table.id == order.table_id).first()

    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    # Yangi buyurtma yaratish
    new_order = Order(
        user_id=Authorize.get_jwt_subject(),  # JWT tokenidan user_id olish
        menu_id=order.menu_id,
        table_id=order.table_id,
        quantity=order.quantity,
        status=order.status,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

@order_router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Buyurtma olish
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")
    return order

@order_router.get("/", response_model=schemas.OrderHistory)
def get_user_orders(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Foydalanuvchining barcha buyurtmalarini olish
    orders = db.query(models.Order).filter(models.Order.user_id == current_user.id).all()
    return {"orders": orders}

@order_router.put("/{order_id}", response_model=schemas.OrderResponse)
def update_order(order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Buyurtma yangilash
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")
    order.status = order_update.status
    db.commit()
    db.refresh(order)
    return order

@order_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Buyurtma o'chirish
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")
    db.delete(order)
    db.commit()
    return None


@order_router.put("/{order_id}", response_model=schemas.OrderResponse)
def update_order(order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    is_nazoratchi(current_user)  # Ruxsatni tekshirish
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyurtma topilmadi")
    order.status = order_update.status
    db.commit()
    db.refresh(order)
    return order
