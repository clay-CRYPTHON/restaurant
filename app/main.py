from datetime import timedelta

from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from app.routers.auth import auth_router
from app.routers.orders import order_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])


class Settings(BaseModel):
    authjwt_secret_key: str = '77db53cb8e5cf81997d16101e70aec714981e3e8dee5338fe4e16b9f0a4b7821'
    authjwt_access_token_expires: timedelta = timedelta(minutes=60)
    authjwt_refresh_token_expires: timedelta = timedelta(days=7)


@AuthJWT.load_config
def get_config():
    return Settings()




@app.get("/")
async def root():
    return {"message": "Welcome to restaurant project"}