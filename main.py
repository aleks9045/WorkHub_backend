from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from services.auth.routers import router as auth_router
import sys

app = FastAPI()

origins = [
    "*"
]  # Сервера, которые могут отправлять запросы на Backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Access-Control-Allow-Origin",
                   "Access-Control-Allow-Methods", "X-Requested-With",
                   "Authorization", "X-CSRF-Token"]
)  # Побеждаем политику CORS

app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
