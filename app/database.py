from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql+psycopg2://postgres:abbossetdarov@localhost/restaurants_db')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

connection = engine.connect()
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

