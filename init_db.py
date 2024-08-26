from app.database import Base, engine
from app.models import User  # Modelni import qilish

# Barcha modellardan jadvallarni yaratish
Base.metadata.create_all(bind=engine)
