from fastapi import FastAPI
from fastapi import APIRouter
from api.users import user_router
from api.admin import admin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Pizza API', version='0.0.1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(admin_router)

app.include_router(main_router)
