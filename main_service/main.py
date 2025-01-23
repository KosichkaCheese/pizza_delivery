from fastapi import FastAPI
from fastapi import APIRouter
from api.users import user_router
from api.admin import admin_router

app = FastAPI(title='Pizza API', version='0.0.1')

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(admin_router)

app.include_router(main_router)
