from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Menu
from app.schemas import MenuCreate, MenuUpdate
from app.database import get_db
from app.permission import is_nazoratchi

menu_router = APIRouter()

@menu_router.post("/create", dependencies=[Depends(is_nazoratchi)])
async def create_menu_item(menu_item: MenuCreate, db: Session = Depends(get_db)):
    db_menu = Menu(**menu_item.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@menu_router.get("/", dependencies=[Depends(is_nazoratchi)])
async def read_menus(db: Session = Depends(get_db)):
    return db.query(Menu).all()

@menu_router.get("/{menu_id}", dependencies=[Depends(is_nazoratchi)])
async def read_menu(menu_id: int, db: Session = Depends(get_db)):
    return db.query(Menu).filter(Menu.id == menu_id).first()

@menu_router.put("/{menu_id}", dependencies=[Depends(is_nazoratchi)])
async def update_menu(menu_id: int, menu_item: MenuUpdate, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu:
        for key, value in menu_item.dict().items():
            setattr(db_menu, key, value)
        db.commit()
        db.refresh(db_menu)
        return db_menu
    else:
        raise HTTPException(status_code=404, detail="Menu item not found")

@menu_router.delete("/{menu_id}", dependencies=[Depends(is_nazoratchi)])
async def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
        return {"detail": "Menu item deleted"}
    else:
        raise HTTPException(status_code=404, detail="Menu item not found")
