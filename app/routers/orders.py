from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Order, User
from app.dependencies import requires_role, get_db

order_router = APIRouter()


@order_router.post("/make")
def create_order(user_id: int, menu_id: int, quantity: int, db: Session = Depends(get_db), current_user: User = Depends(requires_role("user"))):
    # Buyurtma yaratish
    new_order = Order(user_id=user_id, menu_id=menu_id, quantity=quantity, status="pending")
    db.add(new_order)
    db.commit()
    return {"message": "Order created successfully"}


@order_router.get("/")
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(requires_role("hodim"))):
    # Hodim uchun buyurtmalarni ko‘rish
    orders = db.query(Order).filter(Order.status != 'completed').all()
    return {"orders": orders}


@order_router.post("/orders/{order_id}/complete")
def complete_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(requires_role("hodim"))):
    # Buyurtmani tugatish
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = 'completed'
        db.commit()
        return {"message": "Order completed"}
    raise HTTPException(status_code=404, detail="Order not found")