from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.routers.auth import get_current_user  # Bu sizning JWT autentifikatsiyangiz bo'lsa
from app.permission import is_nazoratchi# Rollar bo'yicha tekshirish uchun

order_router = APIRouter()

@order_router.post("/make", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user), Authorize: AuthJWT = Depends()):
    # Yangi buyurtma yaratish
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")

    new_order = models.Order(**order.dict(), user_id=current_user.id)
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
