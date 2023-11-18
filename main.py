from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from services.auth.routers import router as auth_router
from services.tasks.routers import router as task_router

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

origins = [
    "http://localhost",
    "http://90.156.210.55",
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
app.include_router(task_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

Instrumentator().instrument(app).expose(app)
