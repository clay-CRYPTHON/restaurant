from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import TableCreate, TableUpdate, TableInDB
from app.models import Table
from app.database import get_db
from app.permission import is_nazoratchi
from fastapi_jwt_auth import AuthJWT

table_router = APIRouter()


@table_router.get("/", response_model=List[TableInDB])
def get_tables(db: Session = Depends(get_db)):
    tables = db.query(Table).all()
    return tables


@table_router.post("/create", response_model=TableInDB, dependencies=[Depends(is_nazoratchi)])
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


@table_router.patch("/{table_id}", response_model=TableInDB, dependencies=[Depends(is_nazoratchi)])
def update_table(table_id: int, table: TableUpdate, db: Session = Depends(get_db)):
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
def delete_table(table_id: int, db: Session = Depends(get_db)):
    db_table = db.query(Table).filter(Table.id == table_id).first()
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")

    db.delete(db_table)
    db.commit()
    return db_table
