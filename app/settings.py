# app/settings.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    authjwt_secret_key: str = "supersecretkey"
    # boshqa sozlamalarni shu yerda qo'shishingiz mumkin

