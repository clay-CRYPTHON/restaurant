from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.dialects.postgresql import insert
from app.schemas import TableCreate, TableUpdate, TableInDB
from app.models import Table
from app.database import get_db
from app.permission import is_nazoratchi
from app.models import Module
from app import models
from app.models import Module as SQLAlchemyModule  # SQLAlchemy modelini import qiling
from app.schemas import ModuleSchema, ModuleCreate
from app import schemas


table_router = APIRouter()

def upsert_table(db: Session, table_number: int, description: str, capacity: int, status: str):
    stmt = insert(Table).values(
        table_number=table_number,
        description=description,
        capacity=capacity,
        status=status
    ).on_conflict_do_update(
        index_elements=['table_number'],
        set_={
            'description': description,
            'capacity': capacity,
            'status': status
        }
    )
    db.execute(stmt)
    db.commit()


@table_router.get("/", response_model=List[TableInDB])
async def get_tables(db: Session = Depends(get_db)):
    tables = db.query(Table).all()
    return tables


@table_router.post("/create", response_model=TableInDB, dependencies=[Depends(is_nazoratchi)])
async def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


@table_router.patch("/{table_id}", response_model=TableInDB, dependencies=[Depends(is_nazoratchi)])
async def update_table(table_id: int, table: TableUpdate, db: Session = Depends(get_db)):
    db_table = db.query(Table).filter(Table.id == table_id).first()
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")

    if table.capacity is not None:
        db_table.capacity = table.capacity
    if table.status is not None:
        db_table.status = table.status

    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


@table_router.delete("/{table_id}", response_model=TableInDB, dependencies=[Depends(is_nazoratchi)])
async def delete_table(table_id: int, db: Session = Depends(get_db)):
    db_table = db.query(Table).filter(Table.id == table_id).first()
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")

    db.delete(db_table)
    db.commit()
    return db_table


# Get methodi - barcha etajlarni olish
@table_router.get("/floors", response_model=List[schemas.Floor])
async def get_floors(db: Session = Depends(get_db)):
    return db.query(models.Floor).all()

# Post methodi - yangi etaj yaratish
@table_router.post("/floors", response_model=schemas.Floor)
async def create_floor(floor: schemas.FloorCreate, db: Session = Depends(get_db)):
    # Yangi etaj yaratamiz
    db_floor = models.Floor(name=floor.name)
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)  # ID ni qayta yangilash
    return db_floor  # Yangi ID bilan qaytaramiz


@table_router.post("/modules", response_model=ModuleSchema)
async def create_module(module: ModuleCreate, db: Session = Depends(get_db)):
    # Validate table_id if present
    if module.table_id:
        table = db.query(models.Table).filter(models.Table.id == module.table_id).first()
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")

    db_module = models.Module(**module.dict())  # SQLAlchemy modelini ishlating
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

@table_router.get("/modules", response_model=List[schemas.ModuleSchema])
async def get_modules(db: Session = Depends(get_db)):
    return db.query(models.Module).all()
